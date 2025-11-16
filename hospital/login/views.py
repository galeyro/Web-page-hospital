from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario

# Create your views here.
'''
# MVC = Model View Controller
# MVT = Model Template View

Aqui a la vista se le llama template y el controllador se llama View
'''

# DECORADOR PARA PROTEGER VISTAS
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

# DECORADOR PARA VALIDAR ROLES
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
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        
        wrapper.__name__ = view_func.__name__
        wrapper.__doc__ = view_func.__doc__
        return wrapper
    return decorator

# Redirect functions for nav ----------------------------
def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    return render(request, 'home.html')

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

# Ver usuarios de DB
@rol_required('admin')
def control_users(request):
    # Obtener TODOS los usuarios de la DB
    usuarios = Usuario.objects.all()

    # Enviar los usuarios al template
    context = {
        'usuarios': usuarios
    }
    return render(request, 'control_users.html', context)

@rol_required('medico')
def dashboard_medico(request):
    return render(request, 'dashboard_medico.html')

@rol_required('usuario')
def dashboard_usuario(request):
    return render(request, 'dashboard_usuario.html')

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