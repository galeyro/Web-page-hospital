from rest_framework import serializers
from citas.models import Cita

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'