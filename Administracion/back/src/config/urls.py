"""Rutas raíz del back de Administración. Cada módulo se monta bajo /api/v1/."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("cuenta.urls")),
    path("api/v1/sedes/", include("sede.urls")),
    path("api/v1/clinicas/", include("clinica.urls")),
    path("api/v1/personal-clinica/", include("personal_clinica.urls")),
    path("api/v1/", include("socio.urls")),
]
