from django.utils import timezone
from datetime import timedelta
from ..models import Cita, Horario, Medico, Consultorio
from .interfaces import ICitaService

class CitaService(ICitaService):

    def buscar_disponibilidad(self, fecha, especialidad):
        dia_semana = fecha.weekday()
        duracion = especialidad.duracion_cita

        medicos = Medico.objects.filter(especialidad=especialidad)

        for medico in medicos:
            horarios = Horario.objects.filter(
                medico=medico,
                dia_semana=dia_semana
            )

            citas_existentes = Cita.objects.filter(
                medico=medico,
                fecha=fecha
            ).order_by("hora_inicio")

            for horario in horarios:
                hora_actual = horario.hora_inicio

                if fecha == timezone.localdate():
                    hora_real = timezone.localtime().time()
                    while hora_actual < hora_real:
                        hora_actual = self.sumar_minutos(hora_actual, duracion)

                while self.sumar_minutos(hora_actual, duracion) <= horario.hora_fin:
                    hora_fin = self.sumar_minutos(hora_actual, duracion)

                    if not self.hay_conflicto(hora_actual, hora_fin, citas_existentes):
                        consultorio = self.asignar_consultorio(
                            medico, fecha, hora_actual, hora_fin
                        )
                        if consultorio:
                            return medico, hora_actual, hora_fin, consultorio

                    hora_actual = hora_fin

        return None

    def sumar_minutos(self, hora, minutos):
        from datetime import datetime
        dt = datetime.combine(datetime.today(), hora)
        return (dt + timedelta(minutes=minutos)).time()

    def hay_conflicto(self, inicio, fin, citas):
        for c in citas:
            if not (fin <= c.hora_inicio or inicio >= c.hora_fin):
                return True
        return False

    def asignar_consultorio(self, medico, fecha, inicio, fin):
        if medico.tipo != "externo":
            return medico.consultorio

        consultorios = Consultorio.objects.filter(tipo="externo")
        citas = Cita.objects.filter(
            consultorio__in=consultorios,
            fecha=fecha
        )

        for consultorio in consultorios:
            citas_consultorio = citas.filter(consultorio=consultorio)
            if not self.hay_conflicto(inicio, fin, citas_consultorio):
                return consultorio

        return None
