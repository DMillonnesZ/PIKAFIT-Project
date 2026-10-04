"""Envío de correos del módulo cuenta."""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def enviar_enlace_recuperacion(administrador, uid, token):
    enlace = f"{settings.ADMIN_FRONT_URL}/restablecer-contrasena?uid={uid}&token={token}"
    minutos = settings.PASSWORD_RESET_TIMEOUT // 60
    mensaje = (
        f"Hola {administrador.nombres}:\n\n"
        "Recibimos una solicitud para restablecer tu contraseña de PikaFit.\n"
        f"Usa este enlace en los próximos {minutos} minutos. Solo funciona una vez:\n\n"
        f"{enlace}\n\n"
        "Si no la solicitaste, ignora este correo: tu contraseña no cambiará.\n\n"
        "Equipo PikaFit"
    )
    try:
        send_mail("PikaFit: restablece tu contraseña", mensaje,
                  settings.DEFAULT_FROM_EMAIL, [administrador.correo])
    except Exception:  # el usuario recibe 202 igual; el error queda en el log sin datos personales
        logger.exception(
            "No se pudo enviar el correo de recuperación (cuenta %s)", administrador.pk)
