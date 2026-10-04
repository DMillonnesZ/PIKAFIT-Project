"""Capa HTTP del módulo cuenta: recibe, valida con el serializer, delega en services y responde."""
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .serializers import (
    AdministradorSerializer,
    IniciarSesionSerializer,
    RenovarSesionSerializer,
    RestablecerContrasenaSerializer,
    SolicitarRecuperacionSerializer,
)

SEGUNDOS_ACCESO = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
MENSAJE_RECUPERACION = (
    "Si el correo pertenece a una cuenta activa, te enviaremos un enlace para restablecer tu contraseña."
)


# Utilidades internas
def _validar(serializer_class, request) -> dict:
    """Valida el cuerpo de la petición con el serializer indicado y devuelve los datos limpios."""
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    return dict(serializer.validated_data)


# Sesión
class SesionView(APIView):
    """
    POST   /api/v1/auth/sesion   Inicia sesión (público).
    GET    /api/v1/auth/sesion   Datos y rol de la cuenta con sesión activa (requiere token).
    DELETE /api/v1/auth/sesion   Cierra la sesión (requiere token).
    """

    def get_authenticators(self):
        if self.request.method == "POST":
            return []
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):
        datos = _validar(IniciarSesionSerializer, request)
        resultado = services.iniciar_sesion(datos["correo"], datos["contrasena"])
        respuesta = {
            "token_acceso": resultado["token_acceso"],
            "token_renovacion": resultado["token_renovacion"],
            "tipo_token": "Bearer",
            "expira_en_segundos": SEGUNDOS_ACCESO,
            "usuario": AdministradorSerializer(resultado["usuario"]).data,
        }
        return Response(respuesta, status=status.HTTP_200_OK)

    def get(self, request):
        return Response(AdministradorSerializer(request.user).data, status=status.HTTP_200_OK)

    def delete(self, request):
        services.cerrar_sesion(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RenovarSesionView(APIView):
    """POST /api/v1/auth/sesion/renovar   Entrega un nuevo token de acceso (público)."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        datos = _validar(RenovarSesionSerializer, request)
        token_acceso = services.renovar_sesion(datos["token_renovacion"])
        respuesta = {
            "token_acceso": token_acceso,
            "tipo_token": "Bearer",
            "expira_en_segundos": SEGUNDOS_ACCESO,
        }
        return Response(respuesta, status=status.HTTP_200_OK)


# Recuperación de contraseña
class RecuperacionContrasenaView(APIView):
    """POST /api/v1/auth/contrasena/recuperacion   Solicita el enlace de restablecimiento (público)."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        datos = _validar(SolicitarRecuperacionSerializer, request)
        services.solicitar_recuperacion(datos["correo"])
        return Response({"mensaje": MENSAJE_RECUPERACION}, status=status.HTTP_202_ACCEPTED)


class RestablecimientoContrasenaView(APIView):
    """POST /api/v1/auth/contrasena/restablecimiento   Define la nueva contraseña con el enlace (público)."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        datos = _validar(RestablecerContrasenaSerializer, request)
        services.restablecer_contrasena(datos["uid"], datos["token"], datos["nueva_contrasena"])
        return Response(status=status.HTTP_204_NO_CONTENT)