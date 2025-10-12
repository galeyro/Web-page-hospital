from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Usuario

# Create your views here.
'''
# MVC = Model View Controller
# MVT = Model Template View

Aqui a la vista se le llama template y el controllador se llama View
'''

# Redirect functions for nav ----------------------------
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

# Create user ----------------------------------------------
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
                password=password  # TODO: Encriptar contraseña
            )
            usuario.save()
            messages.success(request, 'Usuario creado exitosamente!')
            return redirect('login')
        
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

            # Verificar contraseñá por ahora sin encriptar TODO: Encriptar
            if usuario.password == password:
                # Login exitoso -> crear sesion
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre']=usuario.nombres
                messages.success(request, f'Bienvenido {usuario.nombres}')
                return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta')

        except Usuario.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese email')
                 
    return render(request, 'login.html')

# Logount
def logout_view(request):
    # Limpiar la sesion
    request.session.flush()
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('index')

# Ver usuarios de DB
def control_users(request):
    # Obtener TODOS los usuarios de la DB
    usuarios = Usuario.objects.all()

    # Enviar los usuarios al template
    context = {
        'usuarios': usuarios
    }
    return render(request, 'control_users.html', context)