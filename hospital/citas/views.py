from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .forms import CitaCreateForm
from .models import Cita, Horario, Medico, Especialidad, Consultorio
# Create your views here.

# Hace la suma de los minutos por los bloques
def sumar_minutos(hora, minutos):
    dt = datetime.combine(datetime.today(), hora)
    return (dt + timedelta(minutes=minutos)).time()

# Permite verificar que no existan 2 citas al misma hora sobrelapadas
def hay_conflicto(inicio, fin, citas):
    for c in citas:
        if not (fin <= c.hora_inicio or inicio >= c.hora_fin):
            return True
    return False

def crear_cita(request):
    if request.method == "POST":
        form = CitaCreateForm(request.POST) # Si se realiza un crear con POST, pasaría este flujo

        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            especialidad = form.cleaned_data["especialidad"]
            duracion = especialidad.duracion_cita # Segun la especialidad escogida por usuario se establece la duración

            dia_semana = fecha.weekday() 

            medicos = Medico.objects.filter(especialidad=especialidad) # Filtra medicos segun la especialidad escogida y los selecciona

            for medico in medicos:
                # Verificamos el horario de los medicos
                horarios = Horario.objects.filter(
                    medico=medico,
                    dia_semana=dia_semana
                )
                
                # Si no tienen horario ese día, pasamos
                if not horarios.exists():
                    continue
                
                # Verificamos las citas existentes por medio en cierta fecha
                citas_existentes = Cita.objects.filter(
                    medico=medico,
                    fecha=fecha
                ).order_by("hora_inicio")

                for horario in horarios:
                    # Establecemos la hora actual como la hora de inicio de los médicos
                    hora_actual = horario.hora_inicio

                    # Hacemos el bucle para hacer las verificaciones de horario
                    while sumar_minutos(hora_actual, duracion) <= horario.hora_fin:
                        hora_fin = sumar_minutos(hora_actual, duracion)

                        # Si no existe sobrelapamiento de citas pasamos la recomenacion de citas a la vista adecuada 
                        if not hay_conflicto(hora_actual, hora_fin, citas_existentes):
                            # Mostrar recomendación
                            return render(request, "citas/confirmar_cita.html", {
                                "fecha": fecha,
                                "hora_inicio": hora_actual,
                                "hora_fin": hora_fin,
                                "especialidad": especialidad,
                                "medico": medico,
                                "consultorio": medico.consultorio,
                            })

                        # Si hay conflictos, ponemos la hora fin calculada como la nueva hora de inicio y seguimos
                        hora_actual = hora_fin

            # Si no hay médico o disponibilidad mismo, mandamos error
            messages.error(request, "No hay disponibilidad para esa fecha.")
            return redirect("crear_cita") # Redirige a esta misma vista

    # Si el metodo es GET, solo creamos el formulario y lo pasamos como argumento a la vista
    else:
        form = CitaCreateForm()

    return render(request, "citas/create_cita.html", {"form": form})

def confirmar_cita(request):
    # Si el usuario hace click a Aceptar, establecemos los datos para crear la cita en la Base de Datos
    if request.method == "POST":
        fecha = request.POST["fecha"]
        medico_id = request.POST["medico_id"]
        especialidad_id = request.POST["especialidad_id"]
        hora_inicio = request.POST["hora_inicio"]
        hora_fin = request.POST["hora_fin"]

        medico = Medico.objects.get(id=medico_id)
        especialidad = Especialidad.objects.get(id=especialidad_id)

        # Crear cita con esos campos
        cita = Cita.objects.create(
            paciente=request.user,    # paciente autenticado, usuario creado en el sistema
            medico=medico,
            consultorio=medico.consultorio,
            especialidad=especialidad,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
        )

        # Si todo sale bien, mandamos mensaje de cita reservada correctamente
        messages.success(request, "Cita reservada correctamente.")
        # redirigimos al dashboard_usuario para mostrar las citas agendadas
        return redirect("dashboard_usuario")

    return redirect("crear_cita")