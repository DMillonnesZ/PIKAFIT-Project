"""Reglas de alta, vigencia y renovación de socios y membresías."""
from datetime import timedelta

from bson import ObjectId
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils import timezone
from pymongo.errors import DuplicateKeyError

from sede import services as sede_services

from .models import Membresia, Plan, Socio


class SocioNoEncontrado(Exception):
    pass


class PlanNoEncontrado(Exception):
    pass


class SedeNoDisponible(Exception):
    pass


class SocioDuplicado(Exception):
    pass


class PlanDuplicado(Exception):
    pass


class RenovacionDisponible(Exception):
    def __init__(self, socio):
        self.socio = socio
        super().__init__("El socio ya existe y su membresía venció; puedes renovarla.")


def _obtener_socio(socio_id):
    if not ObjectId.is_valid(socio_id):
        raise SocioNoEncontrado("El socio no existe.")
    try:
        return Socio.objects.get(pk=ObjectId(socio_id))
    except ObjectDoesNotExist as exc:
        raise SocioNoEncontrado("El socio no existe.") from exc


def _obtener_plan_activo(plan_id):
    if not ObjectId.is_valid(plan_id):
        raise PlanNoEncontrado("El plan no está disponible.")
    try:
        plan = Plan.objects.get(pk=ObjectId(plan_id))
    except ObjectDoesNotExist as exc:
        raise PlanNoEncontrado("El plan no está disponible.") from exc
    if not plan.activo:
        raise PlanNoEncontrado("El plan está inactivo.")
    return plan


def _validar_referencias(datos):
    plan = _obtener_plan_activo(datos["plan_id"])
    try:
        sede = sede_services.obtener_activa_para_asignacion(datos["sede_id"])
    except sede_services.SedeNoEncontrada as exc:
        raise SedeNoDisponible(str(exc)) from exc
    if datos["fecha_fin"] < datos["fecha_inicio"]:
        raise ValueError("La fecha de fin no puede ser anterior a la de inicio.")
    fecha_fin_esperada = datos["fecha_inicio"] + timedelta(days=plan.duracion_dias - 1)
    if datos["fecha_fin"] != fecha_fin_esperada:
        raise ValueError(f"Según el plan, la membresía debe finalizar el {fecha_fin_esperada.isoformat()}.")
    return plan, sede


def listar_planes(*, incluir_inactivos=False):
    planes = Plan.objects.all()
    if not incluir_inactivos:
        planes = planes.filter(activo=True)
    return planes.order_by("nombre")


def crear_plan(datos):
    try:
        return Plan.objects.create(**datos)
    except (IntegrityError, DuplicateKeyError) as exc:
        raise PlanDuplicado("Ya existe un plan con ese nombre.") from exc


def actualizar_plan(plan_id, datos):
    plan = _obtener_plan_activo(plan_id)
    for campo, valor in datos.items():
        setattr(plan, campo, valor)
    try:
        plan.save()
    except (IntegrityError, DuplicateKeyError) as exc:
        raise PlanDuplicado("Ya existe un plan con ese nombre.") from exc
    return plan


def desactivar_plan(plan_id):
    plan = _obtener_plan_activo(plan_id)
    plan.activo = False
    plan.save(update_fields=["activo"])
    return plan


def _socio_existente(dni, correo):
    por_dni = Socio.objects.filter(dni=dni).first()
    por_correo = Socio.objects.filter(correo=correo).first()
    if por_dni and por_correo and por_dni.pk != por_correo.pk:
        raise SocioDuplicado("El DNI y el correo pertenecen a cuentas distintas.")
    return por_dni or por_correo


def _ofrecer_renovacion_si_vencio(socio):
    ultima = Membresia.objects.filter(socio_id=socio.pk).order_by("-fecha_fin").first()
    if ultima and ultima.fecha_fin < timezone.localdate():
        raise RenovacionDisponible(socio)
    raise SocioDuplicado("El DNI o el correo ya está registrado.")


def _crear_membresia(socio, plan, inicio, fin):
    return Membresia.objects.create(
        socio_id=socio.pk, plan_id=plan.pk,
        fecha_inicio=inicio, fecha_fin=fin, activa=True,
    )


def crear_socio_con_membresia(datos):
    normalizados = {**datos, "correo": datos["correo"].strip().lower()}
    plan, sede = _validar_referencias(normalizados)
    existente = _socio_existente(normalizados["dni"], normalizados["correo"])
    if existente:
        if existente.dni != normalizados["dni"] or existente.correo != normalizados["correo"]:
            raise SocioDuplicado("El DNI o el correo ya está asociado a otra cuenta.")
        _ofrecer_renovacion_si_vencio(existente)
    try:
        socio = Socio.objects.create(
            nombres=normalizados["nombres"], apellidos=normalizados["apellidos"],
            dni=normalizados["dni"], correo=normalizados["correo"],
            sede_id=sede.pk, activo=True,
        )
        membresia = _crear_membresia(socio, plan, normalizados["fecha_inicio"], normalizados["fecha_fin"])
    except (IntegrityError, DuplicateKeyError) as exc:
        raise SocioDuplicado("El DNI o el correo ya está registrado.") from exc
    return socio, membresia


def renovar_membresia(socio_id, datos):
    socio = _obtener_socio(socio_id)
    normalizados = {**datos, "correo": datos["correo"].strip().lower()}
    if normalizados["dni"] != socio.dni or normalizados["correo"] != socio.correo:
        raise SocioDuplicado("La renovación debe conservar el DNI y el correo del socio.")
    ultima = Membresia.objects.filter(socio_id=socio.pk).order_by("-fecha_fin").first()
    if not ultima or ultima.fecha_fin >= timezone.localdate():
        raise SocioDuplicado("La membresía todavía no ha vencido.")
    plan, sede = _validar_referencias(normalizados)
    socio.nombres = normalizados["nombres"]
    socio.apellidos = normalizados["apellidos"]
    socio.sede_id = sede.pk
    socio.activo = True
    socio.save(update_fields=["nombres", "apellidos", "sede_id", "activo"])
    Membresia.objects.filter(socio_id=socio.pk, activa=True).update(activa=False)
    return socio, _crear_membresia(socio, plan, normalizados["fecha_inicio"], normalizados["fecha_fin"])


def listar_socios():
    return Socio.objects.all().order_by("apellidos", "nombres")


def actualizar_socio(socio_id, datos):
    socio = _obtener_socio(socio_id)
    if "sede_id" in datos:
        try:
            sede = sede_services.obtener_activa_para_asignacion(datos["sede_id"])
        except sede_services.SedeNoEncontrada as exc:
            raise SedeNoDisponible(str(exc)) from exc
        datos["sede_id"] = sede.pk
    for campo, valor in datos.items():
        setattr(socio, campo, valor)
    socio.save()
    return socio
