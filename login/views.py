from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import EmailLoginForm, EmailRegisterForm

def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            auth_login(request, user)  # inicia sesión
            return redirect("login:panel")
    else:
        form = EmailLoginForm()
    return render(request, "login/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = EmailRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # opcional: iniciar sesión inmediatamente
            user = None
            try:
                user = form.instance
            except:
                pass
            if user:
                auth_login(request, user)
                return redirect("login:panel")
            return redirect("login:login")
    else:
        form = EmailRegisterForm()
    return render(request, "login/register.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("login:login")


# decorador simple para exigir es_admin
def admin_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not getattr(request.user, "es_admin", False):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("No tienes permisos para ver esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped


@login_required
@admin_required
def panel_view(request):
    # lista de tablas que el panel mostrará (ejemplo)
    tables = [
        {"name": "Pacientes", "url": "/citas/pacientes/"},
        {"name": "Médicos", "url": "/citas/medicos/"},
        {"name": "Citas", "url": "/citas/citas/"},
    ]
    return render(request, "login/panel.html", {"tables": tables})
