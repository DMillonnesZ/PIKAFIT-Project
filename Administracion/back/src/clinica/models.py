"""Clínicas afiliadas. La desactivación conserva el historial."""
from django.db import models


class Clinica(models.Model):
    razon_social = models.CharField(max_length=160)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=30)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "clinicas"
        verbose_name = "clínica"
        verbose_name_plural = "clínicas"

    def __str__(self):
        return self.razon_social
