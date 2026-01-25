from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError
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
            # Convertir string a objeto date para saber el día de la semana (0=Lunes, 6=Domingo)
            fecha_obj = datetime.strptime(fecha_str,'%Y-%m-%d').date()

        #1. Consultorios (con citas anidadas)
        consultorios = Consultorio.objects.all().order_by('numero')
        consultorios_serializer = ConsultorioSchedulerSerializer(
            consultorios,
            many = True,
            context = {'fecha': fecha_str}
        )

        #2. Horarios de Médicos para ese día de la semana
        dia_semana_num = fecha_obj.weekday()
        horarios = Horario.objects.filter(dia_semana=dia_semana_num)
        horarios_serializer = HorarioMedicoSerializer(
            horarios,
            many = True
        )

        #3. Respuesta combinada
        data = {
            'consultorios': consultorios_serializer.data,
            'horarios_disponibles': horarios_serializer.data
        }
        
        return Response(data)
        
class ReprogramarCitaView(APIView):
    def put(self, request, pk):
        #1. Buscar la cita
        try:
            cita = Cita.objects.get(pk=pk)
        except Cita.DoesNotExist:
            return Response({'error': 'Cita no encontrada'}, status=404)

        #2. Leer datos del JSON que envía React
        nuevo_consultorio_id = request.data.get('consultorio_id')
        nueva_fecha = request.data.get('fecha')
        nueva_hora_inicio = request.data.get('hora_inicio')
        nueva_hora_fin = request.data.get('hora_fin')

        #3. Actualizar el objeto (en memoria, sin guardar todavía)
        if nuevo_consultorio_id:
            cita.consultorio_id = nuevo_consultorio_id
        
        if nueva_fecha:
            cita.fecha = nueva_fecha
            
        if nueva_hora_inicio:
            cita.hora_inicio = nueva_hora_inicio
            
        if nueva_hora_fin:
            cita.hora_fin = nueva_hora_fin

        #4. Validar y guardar
        try:
            #full_clean() ejecuta todos los validadores del modelo (def clean)
            cita.full_clean()
            cita.save()

            #devolvemos la cita actualizada para que React refresque la tarjeta
            return Response({
                'status': 'ok',
                'mensaje': 'Cita Reprogramada Exitosamente'
            })

        except ValidationError as e:
            # Si hay errores de validación, devolvemos el mensaje
            return Response({'error': e.message_dict}, status=400)
        except Exception as e:
            # Si hay otro error, devolvemos el mensaje
            return Response({'error': str(e)}, status=500)