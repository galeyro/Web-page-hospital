from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time
from login.models import Usuario
from citas.models import Medico, Especialidad, Consultorio, Horario, Cita
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Seeds the database with test data for Feb 1, 2026 (Cleans existing first)'

    def handle(self, *args, **kwargs):
        target_date = date(2026, 2, 1)
        self.stdout.write(f'Cleaning existing data for {target_date}...')
        
        # LIMPIEZA INICIAL para evitar fantasmas
        Cita.objects.filter(fecha=target_date).delete()

        # 1. Especialidades
        esp_card, _ = Especialidad.objects.get_or_create(nombre='Cardiología', defaults={'duracion_cita': 30})
        esp_derm, _ = Especialidad.objects.get_or_create(nombre='Dermatología', defaults={'duracion_cita': 30})

        # 2. Paciente 
        paciente, _ = Usuario.objects.get_or_create(
            cedula='1721544600', 
            defaults={
                'nombres': 'Galo', 'apellidos': 'Guevara Torres',
                'email': 'galo.test@example.com', 'telefono': '0999999999',
                'fecha_nacimiento': date(1990, 1, 1), 'genero': 'M',
                'password': make_password('1721544600'), 'rol': 'usuario'
            }
        )

        # 3. Consultorios
        cons_101, _ = Consultorio.objects.get_or_create(numero=101, defaults={'tipo': 'interno'})
        cons_201, _ = Consultorio.objects.get_or_create(numero=201, defaults={'tipo': 'externo'})
        cons_202, _ = Consultorio.objects.get_or_create(numero=202, defaults={'tipo': 'externo'})

        # 4. Médicos
        user_med_int, _ = Usuario.objects.get_or_create(
            cedula='1715403003',
            defaults={
                'nombres': 'Dr. Interno', 'apellidos': 'Cardiología',
                'email': 'medico.interno@hospital.com', 'telefono': '0988888888',
                'fecha_nacimiento': date(1985, 5, 20), 'genero': 'M',
                'password': make_password('1715403003'), 'rol': 'medico'
            }
        )
        med_int, _ = Medico.objects.get_or_create(
            usuario=user_med_int,
            defaults={'especialidad': esp_card, 'tipo': 'interno', 'consultorio': cons_101}
        )

        user_med_ext, _ = Usuario.objects.get_or_create(
            cedula='1710034068',
            defaults={
                'nombres': 'Dr. Externo', 'apellidos': 'Dermatología',
                'email': 'medico.externo@hospital.com', 'telefono': '0977777777',
                'fecha_nacimiento': date(1980, 10, 10), 'genero': 'M',
                'password': make_password('1710034068'), 'rol': 'medico'
            }
        )
        med_ext, _ = Medico.objects.get_or_create(
            usuario=user_med_ext,
            defaults={'especialidad': esp_derm, 'tipo': 'externo'}
        )

        # 5. Horarios (Domingo)
        Horario.objects.update_or_create(medico=med_int, dia_semana=6, defaults={'hora_inicio': time(7, 0), 'hora_fin': time(15, 0)})
        Horario.objects.update_or_create(medico=med_ext, dia_semana=6, defaults={'hora_inicio': time(8, 0), 'hora_fin': time(18, 0)})

        # 6. Citas limpias
        citas_data = [
            (med_int, time(8, 0), time(8, 30), cons_101, esp_card),
            (med_int, time(8, 30), time(9, 0), cons_101, esp_card),
            (med_int, time(13, 0), time(13, 30), cons_101, esp_card),
            (med_ext, time(9, 0), time(9, 30), cons_201, esp_derm),
            (med_ext, time(9, 30), time(10, 0), cons_202, esp_derm),
            (med_ext, time(11, 0), time(11, 30), cons_201, esp_derm),
        ]

        for medico, h_ini, h_fin, cons, esp in citas_data:
            Cita.objects.create(
                medico=medico, paciente=paciente, fecha=target_date,
                hora_inicio=h_ini, hora_fin=h_fin,
                especialidad=esp, consultorio=cons
            )

        self.stdout.write(self.style.SUCCESS(f'Database cleaned and seeded for {target_date}'))
