from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from citas.models import Cita, Consultorio
from citas.services.serializers import *



class SchedulerDataView(APIView):
    def get(self, request):
        fecha_str = request.query_params.get('fecha')
        if not fecha_str:
            fecha_str = date.today().strftime('%Y-%m-%d')
        try:
            consultorios = Consultorio.objects.all().order_by('numero')
            serializer = ConsultorioSchedulerSerializer(
                consultorios,
                many = True,
                context = {'fecha': fecha_str}
            )
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        return Response(serializer.data)
        