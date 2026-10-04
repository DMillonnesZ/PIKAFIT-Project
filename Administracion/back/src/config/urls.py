"""Rutas raíz del back de Administración. Cada módulo se monta bajo /api/v1/."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("cuenta.urls")),
]