import re

from rest_framework import serializers
from django_mongodb_extensions.rest_framework import MongoModelSerializer

from .models import Clinica


def validar_ruc(ruc):
    # Estructura de RUC peruano y su dígito verificador.
    if not re.fullmatch(r"(10|15|20)[0-9]{9}", ruc or ""):
        raise serializers.ValidationError("El RUC debe tener 11 dígitos y un prefijo válido.")
    pesos = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
    diferencia = 11 - sum(int(digito) * peso for digito, peso in zip(ruc[:10], pesos)) % 11
    verificador = diferencia if diferencia < 10 else diferencia - 10
    if verificador != int(ruc[-1]):
        raise serializers.ValidationError("El dígito verificador del RUC no es válido.")
    return ruc


class ClinicaEntradaSerializer(serializers.Serializer):
    razon_social = serializers.CharField(max_length=160, trim_whitespace=True)
    ruc = serializers.CharField(max_length=11, validators=[validar_ruc])
    direccion = serializers.CharField(max_length=255, trim_whitespace=True)
    telefono = serializers.CharField(max_length=30, trim_whitespace=True)
    activa = serializers.BooleanField(required=True)


class ClinicaSalidaSerializer(MongoModelSerializer):
    class Meta:
        model = Clinica
        fields = ["id", "razon_social", "ruc", "direccion", "telefono", "activa"]
        read_only_fields = fields
