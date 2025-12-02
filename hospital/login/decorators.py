# hospital/login/decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from .models import Usuario

def login_required(view_func):
    """
    Decorador que verifica si el usuario está logueado.
    Si no está logueado, redirige al login.
    """
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper

def rol_required(rol_requerido):
    """
    Decorador que verifica si el usuario tiene el rol necesario.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if 'usuario_id' not in request.session:
                messages.warning(request, 'Debes iniciar sesión')
                return redirect('login')
            
            try:
                usuario = Usuario.objects.get(id=request.session['usuario_id'])
                if usuario.rol != rol_requerido:
                    messages.error(request, f'No tienes permisos. Se requiere rol: {rol_requerido}')
                    return redirect('index')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
                return redirect('login')
            
            return view_func(request, *args, **kwargs)
        
        wrapper.__name__ = view_func.__name__
        wrapper.__doc__ = view_func.__doc__
        return wrapper
    return decorator