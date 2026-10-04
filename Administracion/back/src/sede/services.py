"""Reglas de negocio del catálogo de sedes."""
from bson import ObjectId
from django.core.exceptions import ObjectDoesNotExist

from .models import Sede


class SedeNoEncontrada(Exception):
    pass


def _obtener(sede_id):
    if not ObjectId.is_valid(sede_id):
        raise SedeNoEncontrada("La sede no existe.")
    try:
        return Sede.objects.get(pk=ObjectId(sede_id))
    except ObjectDoesNotExist as exc:
        raise SedeNoEncontrada("La sede no existe.") from exc


def listar():
    return Sede.objects.all().order_by("nombre")


def listar_activas():
    """Consulta reutilizable por HU-015 y HU-057 para nuevas asignaciones."""
    return Sede.objects.filter(activa=True).order_by("nombre")


def crear(datos):
    return Sede.objects.create(**datos)


def actualizar(sede_id, datos):
    sede = _obtener(sede_id)
    for campo, valor in datos.items():
        setattr(sede, campo, valor)
    sede.save()
    return sede


def desactivar(sede_id):
    """No elimina el documento: las referencias históricas siguen disponibles."""
    sede = _obtener(sede_id)
    sede.activa = False
    sede.save(update_fields=["activa"])
    return sede


def obtener_activa_para_asignacion(sede_id):
    sede = _obtener(sede_id)
    if not sede.activa:
        raise SedeNoEncontrada("La sede no está disponible para nuevas asignaciones.")
    return sede
