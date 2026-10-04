"""Roles del personal. Fuente única: la usan el modelo, el JWT y los permisos."""
from django.db import models


class Rol(models.TextChoices):
    ADMINISTRADOR_GIMNASIO = "administrador_gimnasio", "Administrador del gimnasio"
    ADMINISTRADOR_CLINICA = "administrador_clinica", "Administrador de la clínica"
    RECEPCIONISTA_CLINICA = "recepcionista_clinica", "Recepcionista de la clínica"


ROLES_CLINICA = {Rol.ADMINISTRADOR_CLINICA, Rol.RECEPCIONISTA_CLINICA}