"""Modelo de la colección administradores (personal del gimnasio y de las clínicas)."""
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django_mongodb_backend.fields import ObjectIdField

from .managers import AdministradorManager
from .roles import ROLES_CLINICA, Rol


class Administrador(AbstractBaseUser):
    """Cuenta del personal del gimnasio o de una clínica afiliada. Colección: administradores."""

    correo = models.EmailField(unique=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    rol = models.CharField(max_length=30, choices=Rol.choices)
    # Referencia a "clinicas". Su existencia la valida el módulo clinica.
    clinica_id = ObjectIdField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    # Se incrementa al cerrar sesión o cambiar la contraseña: invalida todos los JWT emitidos antes.
    version_sesion = models.PositiveIntegerField(default=0)
    es_superusuario = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    # Campos heredados de AbstractBaseUser, renombrados en la base para mantener el español
    password = models.CharField("contraseña", max_length=128, db_column="contrasena_hash")
    last_login = models.DateTimeField("último acceso", null=True, blank=True, db_column="ultimo_acceso")

    objects: AdministradorManager = AdministradorManager()

    USERNAME_FIELD = "correo"
    EMAIL_FIELD = "correo"
    REQUIRED_FIELDS = ["nombres", "apellidos"]

    class Meta:
        db_table = "administradores"
        verbose_name = "administrador"
        verbose_name_plural = "administradores"

    def __str__(self):
        return f"{self.correo} ({self.rol})"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}".strip()

    # Compatibilidad con Django (auth, /admin interno y simplejwt)
    @property
    def is_active(self):
        return self.activo

    @property
    def is_staff(self):
        return self.es_superusuario

    @property
    def is_superuser(self):
        return self.es_superusuario

    def has_perm(self, perm, obj=None):
        return self.activo and self.es_superusuario

    def has_module_perms(self, app_label):
        return self.activo and self.es_superusuario

    # Validaciones del documento
    def clean(self):
        super().clean()
        self.correo = (self.correo or "").strip().lower()
        if self.rol in ROLES_CLINICA and not self.clinica_id:
            raise ValidationError({"clinica_id": "El rol seleccionado requiere una clínica asignada."})
        if self.rol == Rol.ADMINISTRADOR_GIMNASIO and self.clinica_id:
            raise ValidationError({"clinica_id": "El administrador del gimnasio no puede estar asignado a una clínica."})