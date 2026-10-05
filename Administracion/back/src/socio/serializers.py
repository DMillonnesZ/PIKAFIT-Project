import re

from rest_framework import serializers

from .models import Membresia, Plan, Socio


class PlanEntradaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100, trim_whitespace=True)
    duracion_dias = serializers.IntegerField(min_value=1, max_value=3650)
    precio = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    activo = serializers.BooleanField(required=True)


class PlanSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "nombre", "duracion_dias", "precio", "activo"]
        read_only_fields = fields


class SocioEntradaSerializer(serializers.Serializer):
    nombres = serializers.CharField(max_length=100, trim_whitespace=True)
    apellidos = serializers.CharField(max_length=120, trim_whitespace=True)
    dni = serializers.RegexField(re.compile(r"^[0-9]{8}$"), error_messages={"invalid": "El DNI debe tener 8 dígitos."})
    correo = serializers.EmailField()
    sede_id = serializers.CharField()
    plan_id = serializers.CharField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()


class SocioEdicionSerializer(serializers.Serializer):
    nombres = serializers.CharField(max_length=100, trim_whitespace=True, required=False)
    apellidos = serializers.CharField(max_length=120, trim_whitespace=True, required=False)
    sede_id = serializers.CharField(required=False)


class SocioSalidaSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    sede_id = serializers.CharField(read_only=True)
    class Meta:
        model = Socio
        fields = ["id", "nombres", "apellidos", "dni", "correo", "sede_id", "activo"]
        read_only_fields = fields


class MembresiaSalidaSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    socio_id = serializers.CharField(read_only=True)
    plan_id = serializers.CharField(read_only=True)
    class Meta:
        model = Membresia
        fields = ["id", "socio_id", "plan_id", "fecha_inicio", "fecha_fin", "activa"]
        read_only_fields = fields
