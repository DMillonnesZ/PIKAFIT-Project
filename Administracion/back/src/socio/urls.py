from django.urls import path

from .views import PlanDetalleVista, PlanesVista, SocioDetalleVista, SociosVista

urlpatterns = [
    path("planes/", PlanesVista.as_view(), name="planes"),
    path("planes/<str:plan_id>/", PlanDetalleVista.as_view(), name="plan-detalle"),
    path("socios/", SociosVista.as_view(), name="socios"),
    path("socios/<str:socio_id>/", SocioDetalleVista.as_view(), name="socio-detalle"),
]
