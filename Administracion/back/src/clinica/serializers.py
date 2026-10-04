import re

from rest_framework import serializers
from django_mongodb_extensions.rest_framework import MongoModelSerializer

from .models import Clinica


def validar_ruc(ruc):
    # SUNAT: 11 dígitos; 10 y 15 identifican personas, 20 personas jurídicas.
    if not re.fullmatch(r"(10|15|20)[0-9]{9}", ruc or ""):
        raise serializers.ValidationError("El RUC debe tener 11 dígitos y un prefijo válido.")
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
