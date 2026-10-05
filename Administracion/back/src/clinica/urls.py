from django.urls import path

from .views import ClinicaDetalleVista, ClinicasVista


urlpatterns = [
    path("", ClinicasVista.as_view(), name="clinicas"),
    path("<str:clinica_id>/", ClinicaDetalleVista.as_view(), name="clinica-detalle"),
]
