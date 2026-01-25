from rest_framework import serializers
from citas.models import Cita, Consultorio, Horario, Medico

# 1. Serializador para cards de citas
class CitaSchedulerSerializer(serializers.ModelSerializer):
    nombre_medico = serializers.CharField(source='medico.nombre_completo')
    tipo_medico = serializers.CharField(source='medico.tipo')
    nombre_paciente = serializers.CharField(source='paciente.__str__')
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

# 3. Serializador para obtener horarios disponibles
class HorarioMedicoSerializer(serializers.ModelSerializer):
    nombre_medico = serializers.CharField(source='medico.nombre_completo', read_only=True)
    id_medico = serializers.IntegerField(source='medico.id', read_only=True)
    class Meta:
        model = Horario
        fields = [
            'id', 
            'id_medico', 
            'nombre_medico', 
            'dia_semana', 
            'hora_inicio', 
            'hora_fin'
        ]