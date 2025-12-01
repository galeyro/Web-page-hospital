from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .forms import CitaCreateForm
from .models import Cita, Horario, Medico, Especialidad
from login.models import Usuario
# Create your views here.

def login_required(view_func):
    """
    Decorador que verifica si el usuario está logueado.
    Si no está logueado, redirige al login.
    """
    def wrapper(request, *args, **kwargs):
        # Verificar si existe una sesión activa
        if 'usuario_id' not in request.session:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página')
            return redirect('login')
        
        # Si está logueado, ejecutar la vista normalmente
        return view_func(request, *args, **kwargs)
    
    # Mantener el nombre y documentación de la función original
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper

def rol_required(rol_requerido):
    """
    Decorador que verifica si el usuario tiene el rol necesario.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Primero verifica si está logueado
            if 'usuario_id' not in request.session:
                messages.warning(request, 'Debes iniciar sesión')
                return redirect('login')
            
            # Obtener el usuario y su rol
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            
            # Verificar si tiene el rol correcto
            if usuario.rol != rol_requerido:
                messages.error(request, f'No tienes permisos. Se requiere rol: {rol_requerido}')
                return redirect('index')
            
            return view_func(request, *args, **kwargs)
        
        wrapper.__name__ = view_func.__name__
        wrapper.__doc__ = view_func.__doc__
        return wrapper
    return decorator

# Función para normalizar fechas y horas
# TODO: mandar algunas funciones utilitarias como el login_required decorator creado y rol_required creado, a una carpeta utilitaria
def normalizar_fecha_hora(fecha_str, hora_ini_str, hora_fin_str):
    # --- Fecha ---
    # Limpia puntos en meses tipo "Dec." -> "Dec"
    fecha_str = fecha_str.replace(".", "")
    
    # Convierte la fecha obtenida a datetime
    fecha = datetime.strptime(fecha_str, "%b %d, %Y")
    fecha_final = fecha.strftime("%Y-%m-%d")

    # --- Hora inicio ---
    hora_ini_str = hora_ini_str.replace(".", "").strip().lower()  # "9:30 am"
    hora_ini = datetime.strptime(hora_ini_str, "%I:%M %p")
    hora_ini_final = hora_ini.strftime("%H:%M")

    # --- Hora fin ---
    hora_fin_str = hora_fin_str.replace(".", "").strip().lower()  # "9:45 am"
    hora_fin = datetime.strptime(hora_fin_str, "%I:%M %p")
    hora_fin_final = hora_fin.strftime("%H:%M")

    return fecha_final, hora_ini_final, hora_fin_final

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

@login_required
@rol_required('usuario')
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

@login_required
@rol_required('usuario')
def confirmar_cita(request):
    if request.method == "POST":
        medico_id = request.POST.get("medico_id")
        especialidad_id = request.POST.get("especialidad_id")
        fecha_str = request.POST.get("fecha") # fecha obtenida del form
        hora_inicio_str = request.POST.get("hora_inicio") # hora inicio obtenida del form
        hora_fin_str = request.POST.get("hora_fin") # hora fin obtenida del form
        # Esto es para obtener las fechas, horas normalizadas a formato que Django reconoce y puede validar
        fecha, hora_inicio, hora_fin = normalizar_fecha_hora(
            fecha_str,
            hora_inicio_str,
            hora_fin_str
        )

        if not (medico_id and especialidad_id and fecha and hora_inicio and hora_fin):
            messages.error(request, "Datos incompletos para crear la cita.")
            return redirect("create_cita")

        medico = Medico.objects.get(pk=medico_id)
        especialidad = Especialidad.objects.get(pk=especialidad_id)

        cita = Cita.objects.create(
            paciente = Usuario.objects.get(id=request.session["usuario_id"]), # Obtiene el usuario de la sesión manual
            medico=medico,
            consultorio=medico.consultorio,
            especialidad=especialidad,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
        )

        messages.success(request, "Cita reservada correctamente.")
        return redirect("dashboard_usuario")

    # Si alguien entra por GET
    return redirect("create_cita")