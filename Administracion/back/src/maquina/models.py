"""Máquinas registradas en las sedes del gimnasio."""
from django.db import models
from django_mongodb_backend.fields import ObjectIdField


class Maquina(models.Model):
    ESTADOS = [
        ("operativa", "Operativa"),
        ("mantenimiento", "En mantenimiento"),
        ("fuera_servicio", "Fuera de servicio"),
    ]

    codigo = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=120)
    numero_serie = models.CharField(max_length=80, unique=True)
    grupo_muscular = models.CharField(max_length=80)
    sede_id = ObjectIdField()
    estado = models.CharField(max_length=20, choices=ESTADOS)
    token_qr = models.CharField(max_length=32, unique=True, editable=False)

    class Meta:
        db_table = "maquinas"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} · {self.nombre}"
