"""Entrada y salida JSON del módulo cuenta. Validan forma y tipo; las reglas de negocio van en services.py."""
from datetime import timezone as dt_timezone

from rest_framework import serializers

CORREO_ERRORES = {
    "required": "Ingresa tu correo electrónico.",
    "blank": "Ingresa tu correo electrónico.",
    "invalid": "Ingresa un correo electrónico válido.",
}


# Entrada
class IniciarSesionSerializer(serializers.Serializer):
    correo = serializers.EmailField(error_messages=CORREO_ERRORES)
    contrasena = serializers.CharField(
        write_only=True, trim_whitespace=False, max_length=128,
        error_messages={"required": "Ingresa tu contraseña.",
                        "blank": "Ingresa tu contraseña."},
    )


class RenovarSesionSerializer(serializers.Serializer):
    token_renovacion = serializers.CharField(
        error_messages={"required": "El token de renovación es obligatorio.",
                        "blank": "El token de renovación es obligatorio."},
    )


class SolicitarRecuperacionSerializer(serializers.Serializer):
    correo = serializers.EmailField(error_messages=CORREO_ERRORES)


class RestablecerContrasenaSerializer(serializers.Serializer):
    ENLACE_INCOMPLETO = {"required": "El enlace de restablecimiento está incompleto.",
                         "blank": "El enlace de restablecimiento está incompleto."}

    uid = serializers.CharField(error_messages=ENLACE_INCOMPLETO)
    token = serializers.CharField(error_messages=ENLACE_INCOMPLETO)
    nueva_contrasena = serializers.CharField(
        write_only=True, trim_whitespace=False, max_length=128,
        error_messages={"required": "Ingresa la nueva contraseña.",
                        "blank": "Ingresa la nueva contraseña."},
    )


# Salida (nunca expone el hash, version_sesion ni es_superusuario)
class AdministradorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    correo = serializers.EmailField(read_only=True)
    nombres = serializers.CharField(read_only=True)
    apellidos = serializers.CharField(read_only=True)
    rol = serializers.CharField(read_only=True)
    organizacion = serializers.SerializerMethodField()
    ultimo_acceso = serializers.DateTimeField(source="last_login", read_only=True,
                                              default_timezone=dt_timezone.utc)

    def get_organizacion(self, obj):
        if obj.clinica_id:
            return {"tipo": "clinica", "clinica_id": str(obj.clinica_id)}
        return {"tipo": "gimnasio", "clinica_id": None}
