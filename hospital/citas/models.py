from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from login.models import Usuario
from .validators import validar_cedula_ecuador


# ===== ESPECIALIDADES =====
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    duracion_cita = models.IntegerField(
        choices=[(15, '15 minutos'), (30, '30 minutos')],
        default=30
    )

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.duracion_cita} min)"


# ===== CONSULTORIOS =====
class Consultorio(models.Model):
    TIPO_CHOICES = [
        ('interno', 'Interno'),
        ('externo', 'Externo'),
    ]

    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Consultorio {self.numero} ({self.tipo})"


# ===== MÉDICOS =====
class Medico(models.Model):
    TIPO_CHOICES = [
        ('interno', 'Médico Interno'),
        ('externo', 'Médico Externo'),
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='medico')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    consultorio = models.ForeignKey(
        Consultorio, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='medicos'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['usuario__nombres']
        
    def nombre_completo(self):
        return f"Dr. {self.usuario.nombres} {self.usuario.apellidos}"

    def clean(self):
        # Validación: si es interno DEBE tener consultorio
        if self.tipo == 'interno' and not self.consultorio:
            raise ValidationError("Los médicos internos DEBEN tener un consultorio asignado.")
        
        # Validación: si es externo NO puede tener consultorio
        if self.tipo == 'externo' and self.consultorio:
            raise ValidationError("Los médicos externos NO pueden tener consultorio asignado.")
        
        # Validación: consultorio debe ser del tipo correcto
        if self.consultorio:
            if self.tipo == 'interno' and self.consultorio.tipo != 'interno':
                raise ValidationError("Los médicos internos solo pueden usar consultorios internos.")
            if self.tipo == 'externo' and self.consultorio.tipo != 'externo':
                raise ValidationError("Los médicos externos solo pueden usar consultorios externos.")
            
            # Validación: Exclusividad (Un consultorio no puede tener dos médicos asignados)
            ocupante = Medico.objects.filter(consultorio=self.consultorio).exclude(pk=self.pk).first()
            if ocupante:
                raise ValidationError(
                    f"El consultorio {self.consultorio.numero} ya está asignado al Dr. {ocupante.usuario.nombres} {ocupante.usuario.apellidos}."
                )

    def __str__(self):
        return f"Dr. {self.usuario.nombres} - {self.especialidad.nombre if self.especialidad else 'Sin especialidad'}"


# ===== HORARIOS =====
class Horario(models.Model):
    DIA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('medico', 'dia_semana')
        ordering = ['dia_semana', 'hora_inicio']

    def clean(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

    def __str__(self):
        return f"{self.medico} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


# ===== CITAS =====
class Cita(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    consultorio = models.ForeignKey(Consultorio, on_delete=models.SET_NULL, null=True, blank=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)  # Desnormalización
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Evita dos citas del mismo médico a la misma hora
        unique_together = ('medico', 'fecha', 'hora_inicio')
        ordering = ['-fecha', 'hora_inicio']
        indexes = [
            models.Index(fields=['medico', 'fecha']),
            models.Index(fields=['paciente', 'fecha']),
        ]

    def clean(self):
        # 0) Normalización de precisión: SQLite a veces maneja microsegundos que causan 'fantasmas'
        if self.hora_inicio:
            self.hora_inicio = self.hora_inicio.replace(second=0, microsecond=0)
        if self.hora_fin:
            self.hora_fin = self.hora_fin.replace(second=0, microsecond=0)

        # 1) Validar que hora_fin > hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

        # 2) Validar que el consultorio no sea Nulo (Cita sin consultorio es invisible y bloquea)
        if not self.consultorio:
             raise ValidationError("No se puede agendar sin un consultorio asignado. Contacte a soporte.")

        # 3) Validar que la duración coincida con la especialidad
        especialidad = self.especialidad or self.medico.especialidad
        dur_min = (self.hora_fin.hour * 60 + self.hora_fin.minute) - (self.hora_inicio.hour * 60 + self.hora_inicio.minute)
        
        if dur_min != especialidad.duracion_cita:
            raise ValidationError(f"Duración incorrecta: {dur_min} min. Debe ser {especialidad.duracion_cita} min.")

        # 4) Validar solapamiento del Médico (Exclusión estricta por PK)
        solapadas_medico = Cita.objects.filter(medico=self.medico, fecha=self.fecha)
        if self.pk:
            # Forzamos conversión para evitar fallos de tipo en SQLite
            curr_pk = int(self.pk)
            solapadas_medico = solapadas_medico.exclude(pk=curr_pk)
            
        solapadas_medico = solapadas_medico.filter(
            Q(hora_inicio__lt=self.hora_fin) & Q(hora_fin__gt=self.hora_inicio)
        )
        
        if solapadas_medico.exists():
            conflicto = solapadas_medico.first()
            # Log para consola runserver
            print(f"DEBUG: Choque de Medico {self.medico.id} Cita {self.pk} vs {conflicto.pk}")
            raise ValidationError(
                f"El médico ya tiene la cita #{conflicto.pk} en el horario "
                f"{conflicto.hora_inicio.strftime('%H:%M')}-{conflicto.hora_fin.strftime('%H:%M')}."
            )

        # 4.1) Validar solapamiento del Consultorio
        solapadas_cons = Cita.objects.filter(consultorio=self.consultorio, fecha=self.fecha)
        if self.pk:
            solapadas_cons = solapadas_cons.exclude(pk=int(self.pk))
            
        solapadas_cons = solapadas_cons.filter(
            Q(hora_inicio__lt=self.hora_fin) & Q(hora_fin__gt=self.hora_inicio)
        )
        
        if solapadas_cons.exists():
            conflicto = solapadas_cons.first()
            raise ValidationError(
                f"Consultorio {self.consultorio.numero} ocupado por {conflicto.medico.usuario.nombres} "
                f"en el rango {conflicto.hora_inicio.strftime('%H:%M')}-{conflicto.hora_fin.strftime('%H:%M')}."
            )

        # 5) Horarios del médico
        dia = self.fecha.weekday()
        horario = Horario.objects.filter(medico=self.medico, dia_semana=dia).first()
        if not horario:
             raise ValidationError(f"El médico no atiende los {self.fecha.strftime('%A')}.")
        
        if not (horario.hora_inicio <= self.hora_inicio and self.hora_fin <= horario.hora_fin):
            h1, h2 = horario.hora_inicio.strftime('%H:%M'), horario.hora_fin.strftime('%H:%M')
            raise ValidationError(f"Fuera de rango laboral ({h1} a {h2}).")

        # 6) Validación Interno/Externo
        if self.medico.tipo == 'interno':
            if self.consultorio != self.medico.consultorio:
                raise ValidationError(f"Médico interno restringido a consultorio {self.medico.consultorio}.")
        else:
            if self.consultorio.tipo != 'externo':
                raise ValidationError("Médico externo requiere consultorio tipo Externo.")

    def __str__(self):
        return f"#{self.id} {self.paciente.nombres} ({self.fecha} {self.hora_inicio})"
