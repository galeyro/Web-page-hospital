from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from datetime import datetime, date
from citas.models import Cita, Consultorio, Horario
from citas.services.serializers import *


class SchedulerDataView(APIView):
    def get(self, request):
        fecha_str = request.query_params.get('fecha')
        if not fecha_str:
            fecha_obj = date.today()
            fecha_str = fecha_obj.strftime('%Y-%m-%d')
        else:
            fecha_str = fecha_str.split('?')[0].split('&')[0]
            fecha_obj = datetime.strptime(fecha_str,'%Y-%m-%d').date()

        # 1. Consultorios (con citas anidadas)
        consultorios = Consultorio.objects.all().order_by('numero')
        consultorios_serializer = ConsultorioSchedulerSerializer(
            consultorios, many=True, context={'fecha': fecha_str}
        )

        # 2. Horarios de Médicos
        dia_semana_num = fecha_obj.weekday()
        horarios = Horario.objects.filter(dia_semana=dia_semana_num)
        horarios_serializer = HorarioMedicoSerializer(horarios, many=True)

        # 3. DETECCIÓN DE HUÉRFANOS (Citas invisibles)
        huerfanos = Cita.objects.filter(fecha=fecha_str, consultorio__isnull=True)
        huerfanos_data = CitaSchedulerSerializer(huerfanos, many=True).data

        return Response({
            'consultorios': consultorios_serializer.data,
            'horarios_disponibles': horarios_serializer.data,
            'huerfanos': huerfanos_data
        })

class ReprogramarCitaView(APIView):
    def put(self, request, pk):
        try:
            with transaction.atomic():
                # Obtenemos la cita con bloqueo (si fuera Postgres, pero en SQLite ayuda a la atomicidad)
                cita = Cita.objects.get(pk=pk)
                
                nuevo_consultorio_id = request.data.get('consultorio_id')
                nueva_fecha = request.data.get('fecha')
                nueva_hora_ini = request.data.get('hora_inicio')
                nueva_hora_fin = request.data.get('hora_fin')

                if nuevo_consultorio_id:
                    cita.consultorio_id = nuevo_consultorio_id
                if nueva_fecha:
                    cita.fecha = nueva_fecha
                if nueva_hora_ini:
                    cita.hora_inicio = datetime.strptime(nueva_hora_ini[:5], "%H:%M").time()
                if nueva_hora_fin:
                    cita.hora_fin = datetime.strptime(nueva_hora_fin[:5], "%H:%M").time()

                # Ejecutar limpieza y validaciones
                cita.full_clean()
                cita.save()

            return Response({'status': 'ok', 'mensaje': 'Éxito'})

        except ValidationError as e:
            msg = ". ".join(sum(e.message_dict.values(), [])) if hasattr(e, 'message_dict') else str(e)
            return Response({'error': msg}, status=400)
        except Cita.DoesNotExist:
            return Response({'error': 'La cita no existe en la DB.'}, status=404)
        except Exception as e:
            return Response({'error': f"Error fatal: {str(e)}"}, status=500)
