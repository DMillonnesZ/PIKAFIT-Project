"""Socios, membresías y catálogo de planes del gimnasio."""
from django.db import models
from django_mongodb_backend.fields import ObjectIdField


class Plan(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    duracion_dias = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "planes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Socio(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=120)
    dni = models.CharField(max_length=8, unique=True)
    correo = models.EmailField(unique=True)
    sede_id = ObjectIdField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "socios"
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"


class Membresia(models.Model):
    socio_id = ObjectIdField()
    plan_id = ObjectIdField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "membresias"
        ordering = ["-fecha_fin"]

