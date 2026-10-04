"""Creación de cuentas del personal. Siempre guarda el hash de la contraseña, nunca el texto."""
from django.contrib.auth.base_user import BaseUserManager

from .roles import Rol


class AdministradorManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, correo, password=None, **campos):
        if not correo:
            raise ValueError("El correo es obligatorio.")
        usuario = self.model(correo=self.normalize_email(correo).strip().lower(), **campos)
        usuario.set_password(password)
        usuario.full_clean(exclude=["password"])
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **campos):
        """Usado por createsuperuser (solo para el /admin interno de Django)."""
        campos.setdefault("rol", Rol.ADMINISTRADOR_GIMNASIO)
        campos["es_superusuario"] = True
        return self.create_user(correo, password, **campos)