from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField("Correo electrónico", unique=True)
    cedula = models.CharField("Cédula", max_length=30, blank=True, null=True, unique=True)
    telefono = models.CharField("Teléfono", max_length=30, blank=True)
    es_admin = models.BooleanField("Es administrador del sistema", default=False)
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)

    def __str__(self):
        # muestra email si existe, sino username
        return self.email or self.username