from django.urls import path

from .views import MaquinaDetalleVista, MaquinaIdentificarVista, MaquinaQRVista, MaquinasVista


urlpatterns = [
    path("", MaquinasVista.as_view(), name="maquinas"),
    path("identificar/<str:token_qr>/", MaquinaIdentificarVista.as_view(), name="maquina-identificar"),
    path("<str:maquina_id>/qr/", MaquinaQRVista.as_view(), name="maquina-qr"),
    path("<str:maquina_id>/", MaquinaDetalleVista.as_view(), name="maquina-detalle"),
]
