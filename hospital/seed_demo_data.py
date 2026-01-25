import os
import django
from datetime import date, time, timedelta

# Configuración de entorno para script standalone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from login.models import Usuario
from citas.models import Especialidad, Consultorio, Medico, Horario, Cita
from django.contrib.auth.hashers import make_password

def run_seed():
    print("🌱 Iniciando Seed de Datos...")

    # 1. Crear Admin
    if not Usuario.objects.filter(email='admin@admin.com').exists():
        Usuario.objects.create(
            nombres='Admin',
            apellidos='System',
            cedula='0950000000',
            telefono='0900000000',
            email='admin@admin.com',
            fecha_nacimiento='2000-01-01',
            genero='M',
            password=make_password('admin'),
            rol='admin'
        )
        print("✅ Admin creado")
    else:
        print("ℹ️ Admin ya existe")

    # 2. Crear Especialidad
    esp_actor, _ = Especialidad.objects.get_or_create(
        nombre='Doctor Actor',
        defaults={'duracion_cita': 30}
    )
    print(f"✅ Especialidad '{esp_actor.nombre}' lista")

    # 3. Crear Consultorios
    # Internos
    cons_int_1, _ = Consultorio.objects.get_or_create(numero=101, defaults={'tipo': 'interno'})
    cons_int_2, _ = Consultorio.objects.get_or_create(numero=102, defaults={'tipo': 'interno'})
    # Externos
    cons_ext_1, _ = Consultorio.objects.get_or_create(numero=201, defaults={'tipo': 'externo'})
    cons_ext_2, _ = Consultorio.objects.get_or_create(numero=202, defaults={'tipo': 'externo'})
    print("✅ Consultorios creados")

    # 4. Crear Doctores
    # --- Dr. House (Interno) ---
    email_house = 'house@hospital.com'
    if not Usuario.objects.filter(email=email_house).exists():
        user_house = Usuario.objects.create(
            nombres='Gregory',
            apellidos='House',
            cedula='0950000018',
            telefono='0911111111',
            email=email_house,
            fecha_nacimiento='1959-05-15',
            genero='M',
            password=make_password('house123'),
            rol='medico'
        )
        med_house = Medico.objects.create(
            usuario=user_house,
            especialidad=esp_actor,
            tipo='interno',
            consultorio=cons_int_1
        )
        # Horario: Lunes (0) a Viernes (4), 7am - 8pm
        for dia in range(5):
            Horario.objects.create(
                medico=med_house,
                dia_semana=dia,
                hora_inicio=time(7, 0),
                hora_fin=time(20, 0)
            )
        print("✅ Dr. House creado con horarios")
    else:
        med_house = Usuario.objects.get(email=email_house).medico
        print("ℹ️ Dr. House ya existe")

    # --- Dr. Hotel (Externo) ---
    email_hotel = 'hotel@hospital.com'
    if not Usuario.objects.filter(email=email_hotel).exists():
        user_hotel = Usuario.objects.create(
            nombres='Good',
            apellidos='Hotel',
            cedula='0950000026',
            telefono='0922222222',
            email=email_hotel,
            fecha_nacimiento='1980-08-20',
            genero='F',
            password=make_password('hotel123'),
            rol='medico'
        )
        med_hotel = Medico.objects.create(
            usuario=user_hotel,
            especialidad=esp_actor,
            tipo='externo',
            consultorio=None # Externos no tienen consultorio fijo
        )
        # Horario: Lunes (0) a Domingo (6), 9am - 4pm
        # Se agrega Domingo para cubrir fecha Feb 1 2026
        for dia in range(7):
            Horario.objects.create(
                medico=med_hotel,
                dia_semana=dia,
                hora_inicio=time(9, 0),
                hora_fin=time(16, 0)
            )
        print("✅ Dr. Hotel creado con horarios")
    else:
        med_hotel = Usuario.objects.get(email=email_hotel).medico
        print("ℹ️ Dr. Hotel ya existe")

    # 5. Crear Paciente Galo
    email_galo = 'galo@email.com'
    if not Usuario.objects.filter(email=email_galo).exists():
        user_galo = Usuario.objects.create(
            nombres='Galo',
            apellidos='Paciente',
            cedula='0950000034',
            telefono='0933333333',
            email=email_galo,
            fecha_nacimiento='1990-01-01',
            genero='M',
            password=make_password('test'),
            rol='usuario'
        )
        print("✅ Usuario Galo creado")
    else:
        user_galo = Usuario.objects.get(email=email_galo)
        print("ℹ️ Usuario Galo ya existe")

    # 6. Crear Citas (Feb 1 y 2 de 2026)
    # Fechas especificas
    fechas_citas = [date(2026, 2, 1), date(2026, 2, 2)]
    
    for fecha in fechas_citas:
        dia_semana = fecha.weekday() # 0=Mon, 6=Sun
        
        # Intentar agendar con House (Solo L-V)
        if dia_semana < 5: 
            if not Cita.objects.filter(medico=med_house, fecha=fecha).exists():
                try:
                    Cita.objects.create(
                        paciente=user_galo,
                        medico=med_house,
                        consultorio=med_house.consultorio,
                        especialidad=med_house.especialidad,
                        fecha=fecha,
                        hora_inicio=time(8, 0), # 8:00 AM
                        hora_fin=time(8, 30)
                    )
                    print(f"✅ Cita creada con House para {fecha}")
                except Exception as e:
                    print(f"⚠️ No se pudo crear cita House {fecha}: {e}")

        # Intentar agendar con Hotel (L-D segun nuestro seed)
        if not Cita.objects.filter(medico=med_hotel, fecha=fecha).exists():
            try:
                # Para externo, asignamos un consultorio externo libre
                # En un caso real, esto se elige en el momento. Aqui hardcodeamos.
                consultorio_cita = cons_ext_1  
                
                Cita.objects.create(
                    paciente=user_galo,
                    medico=med_hotel,
                    consultorio=consultorio_cita,
                    especialidad=med_hotel.especialidad,
                    fecha=fecha,
                    hora_inicio=time(10, 0), # 10:00 AM
                    hora_fin=time(10, 30)
                )
                print(f"✅ Cita creada con Hotel para {fecha}")
            except Exception as e:
                print(f"⚠️ No se pudo crear cita Hotel {fecha}: {e}")

    print("🏁 Seed completado exitosamente.")

if __name__ == '__main__':
    run_seed()
