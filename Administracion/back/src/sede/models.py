"""Sedes del gimnasio. Django es el único dueño de escritura."""
from django.db import models


class Sede(models.Model):
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=255)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "sedes"
        verbose_name = "sede"
        verbose_name_plural = "sedes"

    def __str__(self):
        return self.nombre
