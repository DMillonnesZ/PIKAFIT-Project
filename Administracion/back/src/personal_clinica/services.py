"""Alta, edición y desactivación del personal afiliado a una clínica."""
from bson import ObjectId
from django.core.exceptions import ObjectDoesNotExist, ValidationError as DjangoValidationError
from django.db import IntegrityError
from pymongo.errors import DuplicateKeyError

from clinica import services as clinica_services
from core.excepciones import ConflictoException, NegocioException, RecursoNoEncontrado
from cuenta import services as cuenta_services
from cuenta.models import Administrador
from cuenta.roles import ROLES_CLINICA


class PersonalNoEncontrado(RecursoNoEncontrado):
    mensaje = "La cuenta del personal de clínica no existe."


class ClinicaNoDisponible(NegocioException):
    estado = 400
    codigo = "CLINICA_NO_DISPONIBLE"
    mensaje = "Selecciona una clínica afiliada activa."


class CampoDuplicado(ConflictoException):
    codigo = "CAMPO_DUPLICADO"

    def __init__(self, campo):
        super().__init__(
            f"El {campo} ya está registrado.",
            detalles=[{"campo": campo, "mensaje": "Ya existe una cuenta con este valor."}],
        )


def _obtener_personal(cuenta_id):
    if not ObjectId.is_valid(cuenta_id):
        raise PersonalNoEncontrado()
    try:
        cuenta = Administrador.objects.get(pk=ObjectId(cuenta_id))
    except ObjectDoesNotExist as exc:
        raise PersonalNoEncontrado() from exc
    if cuenta.rol not in ROLES_CLINICA:
        raise PersonalNoEncontrado()
    return cuenta


def _clinica_activa(clinica_id):
    try:
        return clinica_services.obtener_activa_para_operacion(clinica_id)
    except clinica_services.ClinicaNoEncontrada as exc:
        raise ClinicaNoDisponible() from exc


def _verificar_unicidad(correo, dni, cuenta_id=None):
    por_correo = Administrador.objects.filter(correo=correo).first()
    if por_correo and str(por_correo.pk) != str(cuenta_id):
        raise CampoDuplicado("correo")
    por_dni = Administrador.objects.filter(dni=dni).first()
    if por_dni and str(por_dni.pk) != str(cuenta_id):
        raise CampoDuplicado("DNI")


def _identificar_duplicado(correo, dni, cuenta_id=None):
    _verificar_unicidad(correo, dni, cuenta_id)
    raise CampoDuplicado("correo o DNI")


def listar(clinica_id=None):
    cuentas = Administrador.objects.filter(rol__in=ROLES_CLINICA)
    if clinica_id:
        if not ObjectId.is_valid(clinica_id):
            raise ClinicaNoDisponible()
        cuentas = cuentas.filter(clinica_id=ObjectId(clinica_id))
    return cuentas.order_by("apellidos", "nombres")


def obtener(cuenta_id):
    return _obtener_personal(cuenta_id)


def crear(datos):
    correo = datos["correo"].strip().lower()
    clinica = _clinica_activa(datos["clinica_id"])
    _verificar_unicidad(correo, datos["dni"])
    try:
        cuenta = Administrador.objects.create_user(
            correo=correo, password=None,
            nombres=datos["nombres"], apellidos=datos["apellidos"], dni=datos["dni"],
            rol=datos["rol"], clinica_id=clinica.pk, activo=True,
        )
    except (DjangoValidationError, IntegrityError, DuplicateKeyError) as exc:
        try:
            _identificar_duplicado(correo, datos["dni"])
        except CampoDuplicado as detalle:
            raise detalle from exc
    # HU-001 envía el enlace para que el usuario defina la contraseña; no se entrega una clave inicial.
    cuenta_services.solicitar_recuperacion(correo)
    return cuenta


def actualizar(cuenta_id, datos):
    cuenta = _obtener_personal(cuenta_id)
    cambios = dict(datos)
    if "correo" in cambios:
        cambios["correo"] = cambios["correo"].strip().lower()
    if "clinica_id" in cambios:
        cambios["clinica_id"] = _clinica_activa(cambios["clinica_id"]).pk
    correo = cambios.get("correo", cuenta.correo)
    dni = cambios.get("dni", cuenta.dni)
    _verificar_unicidad(correo, dni, cuenta.pk)
    correo_cambiado = correo != cuenta.correo
    for campo, valor in cambios.items():
        setattr(cuenta, campo, valor)
    try:
        cuenta.full_clean(exclude=["password"])
        cuenta.save()
    except (DjangoValidationError, IntegrityError, DuplicateKeyError) as exc:
        try:
            _identificar_duplicado(correo, dni, cuenta.pk)
        except CampoDuplicado as detalle:
            raise detalle from exc
    if correo_cambiado and cuenta.activo:
        cuenta_services.solicitar_recuperacion(cuenta.correo)
    return cuenta


def desactivar(cuenta_id):
    cuenta = _obtener_personal(cuenta_id)
    if cuenta.activo:
        cuenta.activo = False
        cuenta.version_sesion += 1
        cuenta.save(update_fields=["activo", "version_sesion"])
    return cuenta
