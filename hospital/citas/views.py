from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from .forms import CitaCreateForm
from .models import Cita, Horario, Medico, Especialidad, Consultorio
from login.models import Usuario
from login.decorators import login_required, rol_required
from .services.factory import get_cita_service
from .services.normalizador import normalizar_fecha_hora

@login_required
@rol_required('usuario')
def crear_cita(request):
    if request.method == "POST":
        form = CitaCreateForm(request.POST)

        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            especialidad = form.cleaned_data["especialidad"]

            service = get_cita_service()
            resultado = service.buscar_disponibilidad(fecha, especialidad)

            if resultado:
                medico, hora_inicio, hora_fin, consultorio = resultado
                return render(request, "citas/confirmar_cita.html", {
                    "fecha": fecha,
                    "hora_inicio": hora_inicio,
                    "hora_fin": hora_fin,
                    "especialidad": especialidad,
                    "medico": medico,
                    "consultorio": consultorio,
                })

            messages.error(request, "No hay disponibilidad para esa fecha.")
            return redirect("create_cita")

    else:
        form = CitaCreateForm()

    return render(request, "citas/create_cita.html", {"form": form})

@login_required
@rol_required('usuario')
def confirmar_cita(request):
    if request.method == "POST":
        medico_id = request.POST.get("medico_id")
        especialidad_id = request.POST.get("especialidad_id")
        consultorio_id = request.POST.get("consultorio_id") # obtener asignación de consultorio de forma dinámica
        fecha_str = request.POST.get("fecha") # fecha obtenida del form
        hora_inicio_str = request.POST.get("hora_inicio") # hora inicio obtenida del form
        hora_fin_str = request.POST.get("hora_fin") # hora fin obtenida del form
        # Esto es para obtener las fechas, horas normalizadas a formato que Django reconoce y puede validar
        fecha, hora_inicio, hora_fin = normalizar_fecha_hora( #OJO SE NORMALIZA
            fecha_str,
            hora_inicio_str,
            hora_fin_str
        )

        if not (medico_id and especialidad_id and fecha and hora_inicio and hora_fin):
            messages.error(request, "Datos incompletos para crear la cita.")
            return redirect("create_cita")

        medico = Medico.objects.get(pk=medico_id)
        especialidad = Especialidad.objects.get(pk=especialidad_id)

        # Asignación dinámica para el consultorio interno o externo
        consultorio = None # por defecto
        # Si el consultorio_id es None, significa que el médico es externo y no tiene consultorio
        if consultorio_id:
            consultorio = Consultorio.objects.get(pk=consultorio_id)
        
        # si el medico es interno
        else:
            consultorio = medico.consultorio

        cita = Cita.objects.create(
            paciente = Usuario.objects.get(id=request.session["usuario_id"]), # Obtiene el usuario de la sesión manual
            medico=medico,
            consultorio=consultorio,
            especialidad=especialidad,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
        )

        messages.success(request, "Cita reservada correctamente.")
        return redirect("dashboard_usuario")

    # Si alguien entra por GET
    return redirect("create_cita")