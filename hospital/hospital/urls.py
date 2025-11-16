"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Impotar app con mis vistas
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('inicio/', views.index, name="inicio"),
    path('', views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('create_user/', views.create_user, name='create_user'),
    path('control_users/',views.control_users,name='control_users'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_user/<int:user_id>/',views.delete_user, name='delete_user'),
    path('update_user/<int:user_id>', views.update_user, name='update_user'),
    path('change_rol/<int:user_id>/', views.change_rol, name='change_rol'),
    path('dashboard_medico/', views.dashboard_medico, name='dashboard_medico'),
    path('dashboard_usuario/', views.dashboard_usuario, name='dashboard_usuario'),
    path('create_medico/', views.create_medico, name='create_medico'),
    path('create_consultorio/', views.create_consultorio, name='create_consultorio'),
    path('create_horario/', views.create_horario, name='create_horario'),
    path('create_especialidad/', views.create_especialidad, name='create_especialidad'),
]
