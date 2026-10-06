from django.urls import path

from .views import PersonalClinicaDetalleVista, PersonalClinicaListaVista


urlpatterns = [
    path("", PersonalClinicaListaVista.as_view(), name="personal-clinica"),
    path("<str:cuenta_id>/", PersonalClinicaDetalleVista.as_view(), name="personal-clinica-detalle"),
]
