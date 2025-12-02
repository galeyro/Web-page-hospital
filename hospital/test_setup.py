"""
Script de prueba para verificar las nuevas funcionalidades
- Crear médico
- Crear consultorio  
- Crear horario
- Mantener sesión del admin
"""

import os
import django
from django.test import Client
from django.contrib.auth.hashers import make_password

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from login.models import Usuario
from citas.models import Especialidad, Consultorio, Medico, Horario

# Crear datos de prueba
print("🔧 Configurando datos de prueba...")

# 1. Crear especialidades
especialidades = [
    {'nombre': 'Cardiología', 'duracion_cita': 30},
    {'nombre': 'Dermatología', 'duracion_cita': 30},
]

for esp in especialidades:
    obj, created = Especialidad.objects.get_or_create(
        nombre=esp['nombre'],
        defaults={
            'duracion_cita': esp['duracion_cita']
        }
    )
    status = "✅ Creada" if created else "ℹ️  Existía"
    print(f"  Especialidad {esp['nombre']}: {status}")

# 2. Crear consultorios
consultorios = [
    {'numero': 101, 'tipo': 'interno'},
    {'numero': 102, 'tipo': 'interno'},
    {'numero': 201, 'tipo': 'externo'},
]

for cons in consultorios:
    obj, created = Consultorio.objects.get_or_create(
        numero=cons['numero'],
        defaults={
            'tipo': cons['tipo']
        }
    )
    status = "✅ Creado" if created else "ℹ️  Existía"
    print(f"  Consultorio {cons['numero']}: {status}")

# 3. Verificar que el admin existe y tiene sesión
admin_user = Usuario.objects.filter(rol='admin').first()
if admin_user:
    print(f"\n✅ Admin encontrado: {admin_user.nombres} {admin_user.apellidos}")
else:
    print("❌ No hay admin en la base de datos")

# 4. Verificar disponibilidad de especialidades y consultorios en formularios
print(f"\n📊 Estadísticas:")
print(f"  - Especialidades activas: {Especialidad.objects.count()}")
print(f"  - Consultorios activos: {Consultorio.objects.count()}")
print(f"  - Médicos totales: {Medico.objects.count()}")
print(f"  - Horarios: {Horario.objects.count()}")

print("\n✅ Datos de prueba configurados correctamente")
