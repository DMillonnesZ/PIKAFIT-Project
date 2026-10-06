"""Errores de dominio del módulo cuenta. El formato de respuesta lo arma core.excepciones."""
from core.excepciones import NegocioException


class CredencialesInvalidas(NegocioException):
    estado = 401
    codigo = "CREDENCIALES_INVALIDAS"
    mensaje = "El correo o la contraseña son incorrectos."  # genérico: no revela cuál de los dos falló


class CuentaInactiva(NegocioException):
    estado = 403
    codigo = "CUENTA_INACTIVA"
    mensaje = "Tu cuenta está desactivada. Comunícate con el administrador del gimnasio."


class SesionInvalida(NegocioException):
    estado = 401
    codigo = "SESION_INVALIDA"
    mensaje = "Tu sesión no es válida o ha expirado. Inicia sesión nuevamente."


class EnlaceInvalido(NegocioException):
    estado = 400
    codigo = "ENLACE_INVALIDO_O_VENCIDO"
    mensaje = "El enlace de restablecimiento no es válido, ya fue utilizado o ha expirado. Solicita uno nuevo."