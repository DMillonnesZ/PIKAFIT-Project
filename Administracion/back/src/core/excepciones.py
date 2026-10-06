"""
Excepciones base y manejador global de errores.

Todas las respuestas de error de la API salen con el mismo formato:
{fecha, estado, codigo, mensaje, detalles, ruta}
"""
import logging

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.response import Response

logger = logging.getLogger(__name__)


# Excepciones base de dominio
class NegocioException(Exception):
    """Base de las excepciones de dominio. Cada módulo define las suyas heredando de esta."""

    estado = 422
    codigo = "REGLA_DE_NEGOCIO"
    mensaje = "La operación no cumple una regla de negocio."

    def __init__(self, mensaje=None, detalles=None):
        self.mensaje = mensaje or self.mensaje
        self.detalles = detalles or []
        super().__init__(self.mensaje)


class RecursoNoEncontrado(NegocioException):
    estado = 404
    codigo = "NO_ENCONTRADO"
    mensaje = "El recurso solicitado no existe."


class ConflictoException(NegocioException):
    estado = 409
    codigo = "CONFLICTO"
    mensaje = "La operación entra en conflicto con el estado actual del recurso."


# Utilidades internas
def _cuerpo(estado, codigo, mensaje, request, detalles=None):
    return {
        "fecha": timezone.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "estado": estado,
        "codigo": codigo,
        "mensaje": mensaje,
        "detalles": detalles or [],
        "ruta": request.path if request is not None else "",
    }


def _aplanar(detalle, campo="general"):
    """Convierte los errores de validación de DRF en [{campo, mensaje}]."""
    salida = []
    if isinstance(detalle, dict):
        for clave, valor in detalle.items():
            nombre = "general" if clave in ("non_field_errors", "detail") else clave
            salida += _aplanar(valor, nombre)
    elif isinstance(detalle, list):
        for item in detalle:
            salida += _aplanar(item, campo)
    else:
        salida.append({"campo": campo, "mensaje": str(detalle)})
    return salida


def _codigo_y_mensaje(exc):
    if isinstance(exc, exceptions.ValidationError):
        return "DATOS_INVALIDOS", "Algunos datos no son válidos. Revisa los campos indicados."
    if isinstance(exc, exceptions.NotAuthenticated):
        return "NO_AUTENTICADO", "Debes iniciar sesión para acceder a este recurso."
    if isinstance(exc, exceptions.AuthenticationFailed):
        if exc.get_codes() == "user_inactive":
            return "CUENTA_INACTIVA", "Tu cuenta está desactivada. Comunícate con el administrador del gimnasio."
        return "SESION_INVALIDA", "Tu sesión no es válida o ha expirado. Inicia sesión nuevamente."
    if isinstance(exc, exceptions.PermissionDenied):
        return "SIN_PERMISO", "No tienes permisos para realizar esta acción."
    if isinstance(exc, exceptions.NotFound):
        return "NO_ENCONTRADO", "El recurso solicitado no existe."
    if isinstance(exc, exceptions.MethodNotAllowed):
        return "METODO_NO_PERMITIDO", "El método HTTP utilizado no está permitido en este recurso."
    if isinstance(exc, exceptions.Throttled):
        return "DEMASIADAS_SOLICITUDES", "Has realizado demasiadas solicitudes. Inténtalo nuevamente en unos minutos."
    if isinstance(exc, (exceptions.ParseError, exceptions.UnsupportedMediaType)):
        return "PETICION_INVALIDA", "El cuerpo de la petición debe ser un JSON válido."
    return "ERROR", str(exc.detail)


# Manejador global (registrado en settings.REST_FRAMEWORK["EXCEPTION_HANDLER"])
def manejador_global(exc, context):
    """Convierte cualquier excepción de la API en una respuesta con el formato uniforme."""
    request = context.get("request")

    if isinstance(exc, NegocioException):
        return Response(_cuerpo(exc.estado, exc.codigo, exc.mensaje, request, exc.detalles), status=exc.estado)

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, DjangoPermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        codigo, mensaje = _codigo_y_mensaje(exc)
        detalles = _aplanar(exc.detail) if isinstance(exc, exceptions.ValidationError) else []
        cabeceras = {}
        auth_header = getattr(exc, "auth_header", None)
        if auth_header:
            cabeceras["WWW-Authenticate"] = auth_header
        espera = getattr(exc, "wait", None)
        if espera:
            cabeceras["Retry-After"] = str(int(espera))
        return Response(_cuerpo(exc.status_code, codigo, mensaje, request, detalles),
                        status=exc.status_code, headers=cabeceras)

    logger.exception("Error no controlado en %s", request.path if request else "?", exc_info=exc)
    return Response(
        _cuerpo(500, "ERROR_INTERNO", "Ocurrió un error inesperado. Inténtalo nuevamente más tarde.", request),
        status=500,
    )