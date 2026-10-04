"""JWT del personal: access (corto) y refresh (largo) con los datos que necesita el front."""
from rest_framework_simplejwt.tokens import RefreshToken


class TokenPikaFit(RefreshToken):
    @classmethod
    def for_user(cls, usuario):
        token = super().for_user(usuario)  # agrega user_id (texto de 24 caracteres)
        token["correo"] = usuario.correo
        token["nombre"] = usuario.nombre_completo
        token["rol"] = usuario.rol
        token["clinica_id"] = str(usuario.clinica_id) if usuario.clinica_id else None
        token["ver"] = usuario.version_sesion
        return token  # el access copia estos claims automáticamente


def emitir_tokens(usuario):
    refresh = TokenPikaFit.for_user(usuario)
    return {"token_acceso": str(refresh.access_token), "token_renovacion": str(refresh)}