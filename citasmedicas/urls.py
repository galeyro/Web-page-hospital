from django.urls import path
from . import views

urlpatterns = [
    # ESPECIALIDADES
    path("especialidades/", views.especialidad_list, name="especialidad_list"),
    path("especialidades/nuevo/", views.especialidad_create, name="especialidad_create"),
    path("especialidades/<int:pk>/editar/", views.especialidad_edit, name="especialidad_edit"),
    path("especialidades/<int:pk>/eliminar/", views.especialidad_delete, name="especialidad_delete"),

    # MEDICOS
    path("medicos/", views.medico_list, name="medico_list"),
    path("medicos/nuevo/", views.medico_create, name="medico_create"),
    path("medicos/<int:pk>/editar/", views.medico_edit, name="medico_edit"),
    path("medicos/<int:pk>/eliminar/", views.medico_delete, name="medico_delete"),

    # PACIENTES
    path("pacientes/", views.paciente_list, name="paciente_list"),
    path("pacientes/nuevo/", views.paciente_create, name="paciente_create"),
    path("pacientes/<int:pk>/editar/", views.paciente_edit, name="paciente_edit"),
    path("pacientes/<int:pk>/eliminar/", views.paciente_delete, name="paciente_delete"),

    # CONSULTORIOS
    path("consultorios/", views.consultorio_list, name="consultorio_list"),
    path("consultorios/nuevo/", views.consultorio_create, name="consultorio_create"),
    path("consultorios/<int:pk>/editar/", views.consultorio_edit, name="consultorio_edit"),
    path("consultorios/<int:pk>/eliminar/", views.consultorio_delete, name="consultorio_delete"),

    # HORARIOS
    path("horarios/", views.horario_list, name="horario_list"),
    path("horarios/nuevo/", views.horario_create, name="horario_create"),
    path("horarios/<int:pk>/editar/", views.horario_edit, name="horario_edit"),
    path("horarios/<int:pk>/eliminar/", views.horario_delete, name="horario_delete"),

    # CITAS
    path("citas/", views.cita_list, name="cita_list"),
    path("citas/nueva/", views.cita_create, name="cita_create"),
    path("citas/<int:pk>/editar/", views.cita_edit, name="cita_edit"),
    path("citas/<int:pk>/eliminar/", views.cita_delete, name="cita_delete"),
]
