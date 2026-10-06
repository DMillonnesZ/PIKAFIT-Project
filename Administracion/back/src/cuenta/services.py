"""Reglas de negocio de autenticación del personal. No conoce HTTP: recibe datos validados y lanza excepciones de dominio."""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError

from .correos import enviar_enlace_recuperacion
from .clinicas import clinica_disponible
from .excepciones import CredencialesInvalidas, CuentaInactiva, EnlaceInvalido, SesionInvalida
from .models import Administrador
from .tokens import TokenPikaFit, emitir_tokens


# Utilidades internas
def _normalizar(correo):
    return correo.strip().lower()


def _buscar_por_id(id_texto):
    try:
        return Administrador.objects.get(pk=id_texto)
    except (Administrador.DoesNotExist, DjangoValidationError, ValueError, TypeError):
        return None


# Sesión
def iniciar_sesion(correo, contrasena):
    administrador = Administrador.objects.filter(correo=_normalizar(correo)).first()
    if administrador is None:
        make_password(contrasena)  # mismo tiempo de respuesta exista o no el correo
        raise CredencialesInvalidas()
    if not administrador.check_password(contrasena):
        raise CredencialesInvalidas()
    if not administrador.activo:  # solo se informa si la contraseña es correcta
        raise CuentaInactiva()
    if not clinica_disponible(administrador):
        raise CuentaInactiva()
    administrador.last_login = timezone.now()
    administrador.save(update_fields=["last_login"])
    return {**emitir_tokens(administrador), "usuario": administrador}


def renovar_sesion(token_renovacion):
    try:
        refresh = TokenPikaFit(token_renovacion)  # valida firma, vencimiento y tipo "refresh"
    except TokenError:
        raise SesionInvalida()
    administrador = _buscar_por_id(refresh.get("user_id"))
    if (administrador is None or not administrador.activo or not clinica_disponible(administrador)
            or refresh.get("ver") != administrador.version_sesion):
        raise SesionInvalida()
    return emitir_tokens(administrador)["token_acceso"]  # con el rol actualizado


def cerrar_sesion(administrador):
    administrador.version_sesion += 1
    administrador.save(update_fields=["version_sesion"])


# Recuperación de contraseña
def solicitar_recuperacion(correo):
    administrador = Administrador.objects.filter(correo=_normalizar(correo), activo=True).first()
    if administrador is None:
        return  # no se revela si el correo existe
    uid = urlsafe_base64_encode(force_bytes(administrador.pk))
    token = default_token_generator.make_token(administrador)
    enviar_enlace_recuperacion(administrador, uid, token)


def restablecer_contrasena(uid, token, nueva_contrasena):
    try:
        id_texto = force_str(urlsafe_base64_decode(uid))
    except (ValueError, TypeError):
        raise EnlaceInvalido()
    administrador = _buscar_por_id(id_texto)
    # check_token falla si venció (PASSWORD_RESET_TIMEOUT) o si la contraseña ya cambió (un solo uso)
    if administrador is None or not administrador.activo or not default_token_generator.check_token(administrador, token):
        raise EnlaceInvalido()
    try:
        validate_password(nueva_contrasena, user=administrador)
    except DjangoValidationError as error:
        raise ValidationError({"nueva_contrasena": error.messages})
    administrador.set_password(nueva_contrasena)
    administrador.version_sesion += 1  # cierra las sesiones abiertas con la contraseña anterior
    administrador.save(update_fields=["password", "version_sesion"])
