from rest_framework import serializers

from cuenta.roles import Rol


class PersonalEntradaSerializer(serializers.Serializer):
    nombres = serializers.CharField(max_length=80, trim_whitespace=True)
    apellidos = serializers.CharField(max_length=80, trim_whitespace=True)
    dni = serializers.RegexField(r"^[0-9]{8}$", error_messages={"invalid": "El DNI debe tener 8 dígitos."})
    correo = serializers.EmailField()
    rol = serializers.ChoiceField(choices=[Rol.ADMINISTRADOR_CLINICA, Rol.RECEPCIONISTA_CLINICA])
    clinica_id = serializers.CharField()


class PersonalSalidaSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nombres = serializers.CharField(read_only=True)
    apellidos = serializers.CharField(read_only=True)
    dni = serializers.CharField(read_only=True)
    correo = serializers.EmailField(read_only=True)
    rol = serializers.CharField(read_only=True)
    clinica_id = serializers.CharField(read_only=True)
    activo = serializers.BooleanField(read_only=True)
