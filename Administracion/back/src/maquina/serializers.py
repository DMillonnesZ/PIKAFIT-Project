from bson import ObjectId
from django_mongodb_extensions.rest_framework import MongoModelSerializer
from rest_framework import serializers

from .models import Maquina


class MaquinaEntradaSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=40, trim_whitespace=True)
    nombre = serializers.CharField(max_length=120, trim_whitespace=True)
    numero_serie = serializers.CharField(max_length=80, trim_whitespace=True)
    grupo_muscular = serializers.CharField(max_length=80, trim_whitespace=True)
    sede_id = serializers.CharField()
    estado = serializers.ChoiceField(choices=Maquina.ESTADOS)

    def validate_sede_id(self, valor):
        if not ObjectId.is_valid(valor):
            raise serializers.ValidationError("Selecciona una sede válida.")
        return valor


class MaquinaSalidaSerializer(MongoModelSerializer):
    class Meta:
        model = Maquina
        fields = ["id", "codigo", "nombre", "numero_serie", "grupo_muscular", "sede_id", "estado"]
        read_only_fields = fields
