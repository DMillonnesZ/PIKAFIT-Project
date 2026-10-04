"""Campos de serializer compartidos por todos los módulos."""
from datetime import timezone as dt_timezone

from rest_framework import serializers

FORMATO_FECHA_HORA_UTC = "%Y-%m-%dT%H:%M:%SZ"


class FechaHoraUTCField(serializers.DateTimeField):
    """Fecha y hora en UTC con formato ISO-8601 sin fracciones de segundo. Ejemplo: 2026-10-22T05:57:37Z."""

    def __init__(self, **kwargs):
        kwargs.setdefault("format", FORMATO_FECHA_HORA_UTC)
        kwargs.setdefault("default_timezone", dt_timezone.utc)
        super().__init__(**kwargs)
