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
        # 1) Validar que hora_fin > hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

        # 2) Validar que la fecha sea hoy o futura
        today = timezone.localdate()
        if self.fecha < today:
            raise ValidationError("La cita debe ser para hoy o una fecha futura.")

        # 3) Validar que la duración coincida con la especialidad
        start = datetime.combine(self.fecha, self.hora_inicio)
        end = datetime.combine(self.fecha, self.hora_fin)
        duracion_actual = int((end - start).total_seconds() / 60)  # en minutos
        
        especialidad = self.especialidad or self.medico.especialidad
        if duracion_actual != especialidad.duracion_cita:
            raise ValidationError(
                f"La duración debe ser {especialidad.duracion_cita} minutos "
                f"(especialidad: {especialidad.nombre})"
            )

        # 4) Validar que no haya solapamiento con otras citas del médico
        solapadas = Cita.objects.filter(
            medico=self.medico,
            fecha=self.fecha
        ).exclude(pk=self.pk).filter(
            Q(hora_inicio__lt=self.hora_fin) & Q(hora_fin__gt=self.hora_inicio)
        )
        
        if solapadas.exists():
            raise ValidationError("El médico ya tiene una cita que se solapa en este horario.")

        # 5) Validar que la cita esté dentro de los horarios del médico
        dia_semana = self.fecha.weekday()  # 0=Lunes, 6=Domingo
        horario = Horario.objects.filter(medico=self.medico, dia_semana=dia_semana).first()
        
        if not horario:
            raise ValidationError(
                f"El médico {self.medico} no tiene horario registrado para "
                f"{self.fecha.strftime('%A')}"
            )
        
        if not (horario.hora_inicio <= self.hora_inicio and self.hora_fin <= horario.hora_fin):
            raise ValidationError(
                f"La cita debe estar dentro del horario: {horario.hora_inicio}-{horario.hora_fin}"
            )

        # 6) Validar que el consultorio sea el correcto
        if self.medico.tipo == 'interno':
            if not self.consultorio or self.consultorio != self.medico.consultorio:
                raise ValidationError(
                    f"La cita debe ser en el consultorio asignado al médico: "
                    f"{self.medico.consultorio}"
                )
        else:  # externo
            if not self.consultorio or self.consultorio.tipo != 'externo':
                raise ValidationError("Debe seleccionar un consultorio externo disponible.")

    def __str__(self):
        return f"Cita {self.id} - {self.paciente.nombres} con {self.medico} ({self.fecha} {self.hora_inicio})"
