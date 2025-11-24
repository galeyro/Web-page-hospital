from django.contrib import admin
from .models import Especialidad, Consultorio, Medico, Horario, Cita


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_cita', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'activo', 'descripcion')
    list_filter = ('tipo', 'activo')
    search_fields = ('numero',)
    ordering = ('numero',)


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_medico', 'especialidad', 'tipo', 'consultorio')
    list_filter = ('tipo', 'especialidad')
    search_fields = ('usuario__nombres', 'usuario__apellidos')
    readonly_fields = ('fecha_registro', 'usuario')
    ordering = ('usuario__nombres',)

    fieldsets = (
        ('Información Personal', {
            'fields': ('usuario',)
        }),
        ('Información Profesional', {
            'fields': ('especialidad', 'tipo', 'consultorio')
        }),
        ('Estado', {
            'fields': ('fecha_registro',)
        }),
    )

    def get_nombre_medico(self, obj):
        return f"Dr. {obj.usuario.nombres} {obj.usuario.apellidos}"
    get_nombre_medico.short_description = "Médico"

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Ejecuta validaciones antes de guardar
        super().save_model(request, obj, form, change)


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('medico', 'dia_semana_display', 'hora_inicio', 'hora_fin')
    list_filter = ('dia_semana', 'medico__especialidad')
    search_fields = ('medico__usuario__nombres',)
    ordering = ('medico', 'dia_semana')

    fieldsets = (
        ('Médico', {
            'fields': ('medico',)
        }),
        ('Horario', {
            'fields': ('dia_semana', 'hora_inicio', 'hora_fin')
        }),
    )

    def dia_semana_display(self, obj):
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return dias[obj.dia_semana]
    dia_semana_display.short_description = "Día"

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Ejecuta validaciones antes de guardar
        super().save_model(request, obj, form, change)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha', 'hora_inicio', 'estado', 'consultorio')
    list_filter = ('estado', 'fecha', 'medico__especialidad')
    search_fields = ('paciente__nombres', 'medico__usuario__nombres')
    readonly_fields = ('fecha_creacion', 'especialidad')
    ordering = ('-fecha', 'hora_inicio')

    fieldsets = (
        ('Información de la Cita', {
            'fields': ('paciente', 'medico', 'consultorio', 'especialidad')
        }),
        ('Horario', {
            'fields': ('fecha', 'hora_inicio', 'hora_fin')
        }),
        ('Estado', {
            'fields': ('estado', 'razon_cancelacion')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Asignar especialidad automáticamente si no está definida
        if not obj.especialidad and obj.medico:
            obj.especialidad = obj.medico.especialidad
        
        obj.full_clean()  # Ejecuta validaciones antes de guardar
        super().save_model(request, obj, form, change)
