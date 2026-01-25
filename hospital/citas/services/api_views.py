from rest_framework import viewsets
from citas.models import Cita
from citas.services.serializers import CitaSerializer

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().order_by('-fecha')
    serializer_class = CitaSerializer