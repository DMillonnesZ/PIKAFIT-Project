"""Vigencia de la clínica asociada a una cuenta del personal."""
from clinica.models import Clinica

from .roles import ROLES_CLINICA


def clinica_disponible(usuario):
    if usuario.rol not in ROLES_CLINICA:
        return True
    return bool(
        usuario.clinica_id
        and Clinica.objects.filter(pk=usuario.clinica_id, activa=True).exists()
    )
