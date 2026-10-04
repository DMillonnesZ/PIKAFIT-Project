"""Django es dueño de escritura de la colección de clínicas."""
from bson import ObjectId
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from pymongo.errors import DuplicateKeyError

from .models import Clinica


class ClinicaNoEncontrada(Exception):
    pass


class RucDuplicado(Exception):
    pass


def _obtener(clinica_id):
    if not ObjectId.is_valid(clinica_id):
        raise ClinicaNoEncontrada("La clínica no existe.")
    try:
        return Clinica.objects.get(pk=ObjectId(clinica_id))
    except ObjectDoesNotExist as exc:
        raise ClinicaNoEncontrada("La clínica no existe.") from exc


def listar():
    return Clinica.objects.all().order_by("razon_social")


def listar_activas():
    return Clinica.objects.filter(activa=True).order_by("razon_social")


def _verificar_ruc_disponible(ruc, actual_id=None):
    existente = Clinica.objects.filter(ruc=ruc).first()
    if existente and str(existente.pk) != str(actual_id):
        raise RucDuplicado("El RUC ya está registrado.")


def crear(datos):
    _verificar_ruc_disponible(datos["ruc"])
    try:
        return Clinica.objects.create(**datos)
    except (IntegrityError, DuplicateKeyError) as exc:
        raise RucDuplicado("El RUC ya está registrado.") from exc


def actualizar(clinica_id, datos):
    clinica = _obtener(clinica_id)
    if "ruc" in datos:
        _verificar_ruc_disponible(datos["ruc"], clinica.pk)
    for campo, valor in datos.items():
        setattr(clinica, campo, valor)
    try:
        clinica.save()
    except (IntegrityError, DuplicateKeyError) as exc:
        raise RucDuplicado("El RUC ya está registrado.") from exc
    return clinica


def desactivar(clinica_id):
    clinica = _obtener(clinica_id)
    clinica.activa = False
    clinica.save(update_fields=["activa"])
    return clinica


def obtener_activa_para_operacion(clinica_id):
    """Punto de integración para autenticación clínica y validación de pases."""
    clinica = _obtener(clinica_id)
    if not clinica.activa:
        raise ClinicaNoEncontrada("La clínica está inactiva.")
    return clinica
