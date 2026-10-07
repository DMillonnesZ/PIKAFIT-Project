"""Registro de máquinas asociado solo a sedes activas."""
from uuid import uuid4

from bson import ObjectId
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from pymongo.errors import DuplicateKeyError

from core.excepciones import ConflictoException, NegocioException, RecursoNoEncontrado
from sede import services as sede_services

from .models import Maquina


class MaquinaNoEncontrada(RecursoNoEncontrado):
    mensaje = "La máquina no existe."


class SedeNoDisponible(NegocioException):
    estado = 400
    codigo = "SEDE_NO_DISPONIBLE"
    mensaje = "Selecciona una sede activa para registrar la máquina."


class CampoDuplicado(ConflictoException):
    codigo = "CAMPO_DUPLICADO"

    def __init__(self, campo):
        super().__init__(
            f"El {campo} ya está registrado.",
            detalles=[{"campo": campo, "mensaje": "Ya existe una máquina con este valor."}],
        )


def listar():
    return Maquina.objects.all().order_by("codigo")


def obtener(maquina_id):
    if not ObjectId.is_valid(maquina_id):
        raise MaquinaNoEncontrada()
    try:
        return Maquina.objects.get(pk=ObjectId(maquina_id))
    except ObjectDoesNotExist as exc:
        raise MaquinaNoEncontrada() from exc


def identificar(token_qr):
    try:
        return Maquina.objects.get(token_qr=token_qr)
    except ObjectDoesNotExist as exc:
        raise MaquinaNoEncontrada() from exc


def _verificar_duplicados(codigo, numero_serie):
    if Maquina.objects.filter(codigo=codigo).exists():
        raise CampoDuplicado("codigo")
    if Maquina.objects.filter(numero_serie=numero_serie).exists():
        raise CampoDuplicado("numero_serie")


def registrar(datos):
    codigo = datos["codigo"].strip().upper()
    numero_serie = datos["numero_serie"].strip().upper()
    try:
        sede = sede_services.obtener_activa_para_asignacion(datos["sede_id"])
    except sede_services.SedeNoEncontrada as exc:
        raise SedeNoDisponible() from exc
    _verificar_duplicados(codigo, numero_serie)
    try:
        return Maquina.objects.create(
            codigo=codigo,
            nombre=datos["nombre"].strip(),
            numero_serie=numero_serie,
            grupo_muscular=datos["grupo_muscular"].strip(),
            sede_id=sede.pk,
            estado=datos["estado"],
            token_qr=uuid4().hex,
        )
    except (IntegrityError, DuplicateKeyError, ValidationError) as exc:
        try:
            _verificar_duplicados(codigo, numero_serie)
        except CampoDuplicado as detalle:
            raise detalle from exc
        raise
