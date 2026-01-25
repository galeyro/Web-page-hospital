from rest_framework import serializers
from citas.models import Cita, Consultorio

# 1. Serializador para cards de citas
class CitaSchedulerSerializer(serializers.ModelSerializer):
    nombre_medico = serializers.CharField(source='medico.usuario.nombres')
    tipo_medico = serializers.CharField(source='medico.tipo')
    nombre_paciente = serializers.CharField(source='paciente.nombres')
    nombre_especialidad = serializers.CharField(source='especialidad.nombre')
    
    class Meta:
        model = Cita
        fields = [
            'id',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'nombre_medico',
            'tipo_medico',
            'nombre_paciente',
            'nombre_especialidad',
        ]

# 2. Serializador para las columnas (consultorios)
class ConsultorioSchedulerSerializer(serializers.ModelSerializer):
    citas = serializers.SerializerMethodField()
    
    class Meta:
        model = Consultorio
        fields = [
            'id',
            'numero',
            'tipo',
            'citas',
        ]
    
    def get_citas(self, obj):
        # Filtramos citas de este consultorio
        fecha = self.context.get('fecha')
        citas_query = obj.cita_set.all()

        if fecha:
            citas_query = citas_query.filter(fecha=fecha)
        
        return CitaSchedulerSerializer(citas_query, many=True).data