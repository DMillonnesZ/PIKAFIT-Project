"""Autenticación de cada petición protegida mediante la cabecera Authorization: Bearer."""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class AutenticacionJWT(JWTAuthentication):
    """Lee Authorization: Bearer <token_acceso>. Rechaza cuentas inactivas y tokens de sesiones cerradas."""

    def get_user(self, validated_token):
        usuario = super().get_user(validated_token)  # valida que exista y esté activo
        if validated_token.get("ver") != usuario.version_sesion:
            raise AuthenticationFailed("Sesión cerrada.", code="sesion_cerrada")
        return usuario