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

def login_view(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def control_users(request):
    return render(request, 'control_users.html')

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
