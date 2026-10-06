"""Rutas del módulo cuenta. Se montan en config/urls.py bajo /api/v1/auth/."""
from django.urls import path

from .views import (
    RecuperacionContrasenaView,
    RenovarSesionView,
    RestablecimientoContrasenaView,
    SesionView,
)

app_name = "cuenta"

urlpatterns = [
    # Sesión
    path("sesion", SesionView.as_view(), name="sesion"),
    path("sesion/renovar", RenovarSesionView.as_view(), name="renovar-sesion"),
    # Recuperación de contraseña
    path("contrasena/recuperacion", RecuperacionContrasenaView.as_view(), name="recuperacion-contrasena"),
    path("contrasena/restablecimiento", RestablecimientoContrasenaView.as_view(), name="restablecimiento-contrasena"),
]