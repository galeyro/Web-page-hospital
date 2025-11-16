from django.urls import path
from .views import login_view, register_view, logout_view, panel_view

app_name = "login"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("panel/", panel_view, name="panel"),
]
