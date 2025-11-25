import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from login.models import Usuario
from django.contrib.auth.hashers import make_password

# Verificar si el admin ya existe
if not Usuario.objects.filter(email='admin@admin.com').exists():
    admin = Usuario(
        nombres='Admin',
        apellidos='Admin',
        cedula='0950000000',  # Cédula válida ecuatoriana
        telefono='0987654321',
        email='admin@admin.com',
        fecha_nacimiento='2000-01-01',
        genero='M',
        password=make_password('admin'),
        rol='admin'
    )
    admin.save()
    print("✅ Admin creado exitosamente")
else:
    print("⚠️ Admin ya existe")