from django.urls import path

from .views import SedeDetalleVista, SedesVista


urlpatterns = [
    path("", SedesVista.as_view(), name="sedes"),
    path("<str:sede_id>/", SedeDetalleVista.as_view(), name="sede-detalle"),
]
