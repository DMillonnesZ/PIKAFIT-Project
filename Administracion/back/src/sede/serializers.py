from rest_framework import serializers
from django_mongodb_extensions.rest_framework import MongoModelSerializer

from .models import Sede


class SedeEntradaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=120, trim_whitespace=True)
    direccion = serializers.CharField(max_length=255, trim_whitespace=True)
    activa = serializers.BooleanField(required=True)


class SedeSalidaSerializer(MongoModelSerializer):
    class Meta:
        model = Sede
        fields = ["id", "nombre", "direccion", "activa"]
        read_only_fields = fields
