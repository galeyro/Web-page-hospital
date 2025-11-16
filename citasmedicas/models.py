# citasmedicas/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from .choices import PROVINCIAS_EC, SEXOS, ESTATUS_MEDICO, DIAS_SEMANA, ESTADOS_CITA

from .validators import validar_cedula_ecuador

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[validar_cedula_ecuador]
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, blank=True)
    numero_licencia = models.CharField(max_length=50, blank=True)
    estatus = models.CharField(max_length=50, choices=ESTATUS_MEDICO, default="INTERNO")

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido}"


class Paciente(models.Model):
    cedula = models.CharField(max_length=10, unique=True, validators=[validar_cedula_ecuador])
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    correo = models.EmailField()
    sexo = models.CharField(max_length=1, choices=SEXOS)
    provincia = models.CharField(max_length=2, choices=PROVINCIAS_EC, default="17")    
    
    def __str__(self):
        return f"Paciente {self.nombre} {self.apellido}"


class Consultorio(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Consultorio {self.codigo}"


class HorarioMedico(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)  # podrías usar choices para "Lunes", "Martes", etc.
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def clean(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora fin debe ser posterior a la hora inicio.")

    def __str__(self):
        return f"{self.medico} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    consultorio = models.ForeignKey(Consultorio, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CITA, default="PENDIENTE")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        # evita crear dos citas exactamente con mismo medico, misma fecha y misma hora inicio
        unique_together = ("medico", "fecha", "hora_inicio")
        ordering = ["-fecha", "hora_inicio"]

    def clean(self):
        # 1) hora_fin > hora_inicio
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser mayor que la hora de inicio.")

        # 2) fecha debe ser hoy o futura
        today = timezone.localdate()
        if self.fecha < today:
            raise ValidationError("La fecha de la cita debe ser hoy o en el futuro.")

        # 3) evitar solapamiento con otras citas del mismo médico
        from django.db.models import Q
        qs = Cita.objects.filter(
            medico=self.medico,
            fecha=self.fecha
        ).exclude(pk=self.pk)  # excluir esta misma si es edición

        # Si alguna cita existente comienza antes de nuestra hora_fin y termina después de nuestra hora_inicio -> solapamiento
        overlap = qs.filter(
            Q(hora_inicio__lt=self.hora_fin) & Q(hora_fin__gt=self.hora_inicio)
        ).exists()
        if overlap:
            raise ValidationError("El médico ya tiene una cita en el horario seleccionado (solapamiento).")

    def __str__(self):
        return f"Cita {self.pk} - {self.paciente} con {self.medico} el {self.fecha} {self.hora_inicio}"
