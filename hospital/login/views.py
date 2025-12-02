from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import Usuario
from citas.models import Medico, Cita, Especialidad, Consultorio, Horario
from .forms import CreateMedicoForm, CreateConsultorioForm, CreateHorarioForm, CreateEspecialidadForm
from .decorators import login_required, rol_required

# Redirect functions for nav ----------------------------
def index(request):
    return render(request, 'index.html')
# Create user -------------------------------------------
def create_user(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero')
        password = request.POST.get('password')
        password_hash = make_password(password) #Hash
        try:
            # Crear y guardar el usuario
            usuario = Usuario(
                nombres=nombres,
                apellidos=apellidos,
                cedula=cedula,
                telefono=telefono,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero,
                password = password_hash
            )
            usuario.full_clean()  # Ejecuta las validaciones del modelo
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente!')
            
            # Si el que crea es admin, volver al panel de control
            if request.session.get('usuario_rol') == 'admin':
                return redirect('control_users')
                
            return redirect('login')
        
        except ValidationError as e:
            # e.message_dict es un diccionario con los errores por campo
            for campo, errores in e.message_dict.items():
                for error in errores:
                    messages.error(request, f'{campo}: {error}')
        
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')

    return render(request, 'create_user.html')

# Login con usuario y contraseña
def login_view(request):
    if request.method == 'POST':
        # Obtener datos del forms
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Buscar usuario en BD
            usuario = Usuario.objects.get(email=email)

            if check_password(password, usuario.password): #Seguro hash
                # Login exitoso -> crear sesion
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre']=usuario.nombres
                request.session['usuario_rol'] = usuario.rol 
                messages.success(request, f'Bienvenido {usuario.nombres}')
                
                # Redirigir según el rol del usuario
                if usuario.rol == 'admin':
                    return redirect('control_users')
                elif usuario.rol == 'medico':
                    return redirect('dashboard_medico')
                else:  # usuario normal
                    return redirect('dashboard_usuario')
            else:
                messages.error(request, 'Contraseña incorrecta')

        except Usuario.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese email')
                 
    return render(request, 'login.html')

# Logount
def logout_view(request):
    # Limpiar mensajes anteriores primero
    storage = messages.get_messages(request)
    for message in storage:
        # Los mensajes se marcan como leídos
        pass

    # Limpiar la sesion
    request.session.flush()
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('index')

@rol_required('admin')
def control_users(request):
    usuarios = Usuario.objects.all()
    medicos = Medico.objects.select_related('usuario', 'especialidad', 'consultorio')
    citas = Cita.objects.select_related('medico', 'paciente', 'especialidad')
    
    # Estadísticas de usuarios
    total_usuarios = usuarios.count()
    total_admins = usuarios.filter(rol='admin').count()
    total_medicos_usuarios = usuarios.filter(rol='medico').count()
    total_usuarios_normales = usuarios.filter(rol='usuario').count()
    
    # Estadísticas de médicos
    total_medicos_internos = medicos.filter(tipo='interno').count()
    total_medicos_externos = medicos.filter(tipo='externo').count()
    total_medicos_activos = medicos.count()
    
    # Estadísticas de consultorios
    total_consultorios_internos = Consultorio.objects.filter(tipo='interno').count()
    total_consultorios_externos = Consultorio.objects.filter(tipo='externo').count()
    
    # Estadísticas de citas
    total_citas = citas.count()
    
    # Especialidades
    especialidades = Especialidad.objects.all().count()
    
    context = {
        'usuarios': usuarios,
        'medicos': medicos,
        'citas': citas,
        
        # Stats usuarios
        'total_usuarios': total_usuarios,
        'total_admins': total_admins,
        'total_medicos_usuarios': total_medicos_usuarios,
        'total_usuarios_normales': total_usuarios_normales,
        
        # Stats médicos
        'total_medicos_internos': total_medicos_internos,
        'total_medicos_externos': total_medicos_externos,
        'total_medicos_activos': total_medicos_activos,
        
        # Stats consultorios
        'total_consultorios_internos': total_consultorios_internos,
        'total_consultorios_externos': total_consultorios_externos,
        
        # Stats citas
        'total_citas': total_citas,
        
        # Stats especialidades
        'total_especialidades': especialidades,
        
    }
    return render(request, 'control_users.html', context)

@rol_required('admin')
def change_rol(request, user_id):
    if request.method == 'POST':
        nuevo_rol = request.POST.get('nuevo_rol')
        try:
            usuario = Usuario.objects.get(id=user_id)
            rol_anterior = usuario.rol
            usuario.rol = nuevo_rol
            usuario.save()
            messages.success(request, f'Rol de {usuario.nombres} cambió de {rol_anterior} a {nuevo_rol}')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
    
    return redirect('control_users')

# Dashboard para usuarios normales
@rol_required('usuario')
def dashboard_usuario(request):
    # Aquí irán las citas del usuario desde el modelo que crearemos
    # Se obtiene el paciente (usuario) que esta iniciado la sesion
    paciente = Usuario.objects.get(id=request.session["usuario_id"])
    citas = Cita.objects.filter(
        paciente = paciente # Se filtra por ese usuario
    )

    context = {
        'citas': citas  # Se llenará cuando tengamos el modelo de Citas
    }
    return render(request, 'dashboard_usuario.html', context)


# Dashboard para médicos
@rol_required('medico')
def dashboard_medico(request):
    # Completamente relacionadas las citas con los medicos
    usuario = Usuario.objects.get(id=request.session["usuario_id"]) # Obtenemos primero el usuario asignado a la sesion (medico inicio sesión)

    # Obtener la instancia de Medico asociada
    try:
        medico = usuario.medico # Verificamos que sea medico, este registrado como medico
    except Medico.DoesNotExist:
        return HttpResponse("Este usuario no está registrado como médico.")
    
    hoy = timezone.localdate()
    
    # Citas del medico que tiene hoy
    citas_hoy = Cita.objects.filter(
        medico = medico,
        fecha = hoy
    ).order_by('hora_inicio')
    
    # Citas del medico en total, de forma historica
    citas_historial = Cita.objects.filter(
        medico=medico
    ).order_by('-fecha', '-hora_inicio')
    
    context = {
        'citas_hoy': citas_hoy,       # Se llenará cuando tengamos el modelo de Citas
        'citas_historial': citas_historial  # Se llenará cuando tengamos el modelo de Citas
    }
    return render(request, 'dashboard_medico.html', context)

# ===== CREAR MÉDICO =====
@rol_required('admin')
def create_medico(request):
    """Crear un nuevo médico (usuario con rol médico)"""
    if request.method == 'POST':
        form = CreateMedicoForm(request.POST)
        
        if form.is_valid():
            try:
                # Crear usuario
                password_hash = make_password(form.cleaned_data['password'])
                usuario = Usuario(
                    nombres=form.cleaned_data['nombres'],
                    apellidos=form.cleaned_data['apellidos'],
                    cedula=form.cleaned_data['cedula'],
                    telefono=form.cleaned_data['telefono'],
                    email=form.cleaned_data['email'],
                    fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                    genero=form.cleaned_data['genero'],
                    password=password_hash,
                    rol='medico'
                )
                usuario.full_clean()
                usuario.save()
                
                # Crear médico asociado
                medico = Medico(
                    usuario=usuario,
                    especialidad=form.cleaned_data['especialidad'],
                    tipo=form.cleaned_data['tipo'],
                    consultorio=form.cleaned_data.get('consultorio')
                )
                medico.full_clean()
                medico.save()
                
                messages.success(request, f'Médico {usuario.nombres} {usuario.apellidos} creado exitosamente!')
                # Mantener sesión del admin - redirigir a control_users sin cerrar sesión
                return redirect('control_users')
            
            except ValidationError as e:
                for campo, errores in e.message_dict.items():
                    for error in errores:
                        messages.error(request, f'{campo}: {error}')
            except Exception as e:
                messages.error(request, f'Error al crear médico: {str(e)}')
    else:
        form = CreateMedicoForm()
    
    context = {'form': form}
    return render(request, 'create_medico.html', context)

# ===== CREAR CONSULTORIO =====
@rol_required('admin')
def create_consultorio(request):
    """Crear un nuevo consultorio"""
    if request.method == 'POST':
        form = CreateConsultorioForm(request.POST)
        
        if form.is_valid():
            try:
                consultorio = form.save()
                messages.success(request, f'Consultorio {consultorio.numero} creado exitosamente!')
                return redirect('control_users')
            
            except ValidationError as e:
                for campo, errores in e.message_dict.items():
                    for error in errores:
                        messages.error(request, f'{campo}: {error}')
            except Exception as e:
                messages.error(request, f'Error al crear consultorio: {str(e)}')
    else:
        form = CreateConsultorioForm()
    
    context = {'form': form}
    return render(request, 'create_consultorio.html', context)

# ===== CREAR HORARIO =====
@rol_required('admin')
def create_horario(request):
    """Crear un nuevo horario para un médico"""
    if request.method == 'POST':
        form = CreateHorarioForm(request.POST)
        
        if form.is_valid():
            try:
                horario = form.save()
                messages.success(request, f'Horario creado exitosamente!')
                return redirect('control_users')
            
            except ValidationError as e:
                for campo, errores in e.message_dict.items():
                    for error in errores:
                        messages.error(request, f'{campo}: {error}')
            except Exception as e:
                messages.error(request, f'Error al crear horario: {str(e)}')
    else:
        form = CreateHorarioForm()
    
    context = {'form': form}
    return render(request, 'create_horario.html', context)

# ===== CREAR ESPECIALIDAD =====
@rol_required('admin')
def create_especialidad(request):
    """Crear una nueva especialidad"""
    if request.method == 'POST':
        form = CreateEspecialidadForm(request.POST)
        
        if form.is_valid():
            try:
                especialidad = form.save()
                messages.success(request, f'Especialidad {especialidad.nombre} creada exitosamente!')
                return redirect('control_users')
            
            except ValidationError as e:
                for campo, errores in e.message_dict.items():
                    for error in errores:
                        messages.error(request, f'{campo}: {error}')
            except Exception as e:
                messages.error(request, f'Error al crear especialidad: {str(e)}')
    else:
        form = CreateEspecialidadForm()
    
    context = {'form': form}
    return render(request, 'create_especialidad.html', context)

# ===== LISTAR HORARIOS =====
@rol_required('admin')
def list_horarios(request):
    """Listar horarios con filtro por médico"""
    medicos = Medico.objects.select_related('usuario').order_by('usuario__nombres')
    
    medico_id = request.GET.get('medico_id')
    if medico_id:
        horarios = Horario.objects.filter(medico_id=medico_id).select_related('medico', 'medico__usuario').order_by('dia_semana', 'hora_inicio')
    else:
        # Si no hay selección, no mostramos horarios (o podríamos mostrar todos)
        # Según requerimiento: "solo el seleccionado cargue sus horarios"
        horarios = None
    
    context = {
        'medicos': medicos,
        'horarios': horarios,
        'medico_seleccionado': int(medico_id) if medico_id else None
    }
    return render(request, 'list_horarios.html', context)

# Delete specific user from DB
@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            # Buscar usuario por ID
            usuario = Usuario.objects.get(id=user_id)

            # Guardar el nombre para el mensaje
            nombre_usuario = f"{usuario.nombres} {usuario.apellidos}"

            # Eliminar usuario DB
            usuario.delete()
            messages.success(request, f"Usuario {nombre_usuario} eliminado exitosamente")
        
        except Usuario.DoesNotExist:
            messages.error(request,"El usuario no existe")

        except Exception as e:
            messages.error(request, f"Error al eliminar usuario: {str(e)}")
    
    return redirect('control_users')

# Update user as part of CRUD
@login_required
def update_user(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe')
        return redirect('control_users')
    
    if request.method == 'POST':
        # Obtener datos con valores por defecto
        nombres = request.POST.get('nombres', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        cedula = request.POST.get('cedula', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento', '')
        genero = request.POST.get('genero', '')
        password = request.POST.get('password', '').strip()

        # Validaciones
        errores = []
        if not nombres:
            errores.append('El campo nombres es requerido')
        if not apellidos:
            errores.append('El campo apellidos es requerido')
        if not email:
            errores.append('El campo email es requerido')
        if not cedula:
            errores.append('El campo cédula es requerido')
        if not telefono:
            errores.append('El campo teléfono es requerido')

        if errores:
            for error in errores:
                messages.error(request, error)
            context = {'usuario': usuario}
            return render(request, 'update_user.html', context)

        try:
            # Actualizar solo los campos que tienen datos
            usuario.nombres = nombres
            usuario.apellidos = apellidos
            usuario.cedula = cedula
            usuario.telefono = telefono
            usuario.email = email
            
            if fecha_nacimiento:
                usuario.fecha_nacimiento = fecha_nacimiento
            if genero:
                usuario.genero = genero
            if password:
                usuario.password = make_password(password) #hash

            usuario.full_clean()  # Ejecuta las validaciones del modelo
            usuario.save()

            messages.success(request, f"Usuario {usuario.nombres} {usuario.apellidos} actualizado exitosamente")
            return redirect('control_users')
        
        except Exception as e:
            messages.error(request, f"Error al actualizar usuario: {str(e)}")
    
    # Si es GET, mostrar formulario con datos actuales
    context = {'usuario': usuario}
    return render(request, 'update_user.html', context)