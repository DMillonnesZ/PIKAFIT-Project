"""Comando para crear cuentas del personal en entornos de desarrollo y pruebas."""
import getpass

from bson import ObjectId
from bson.errors import InvalidId
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from cuenta.models import Administrador
from cuenta.roles import Rol


class Command(BaseCommand):
    help = "Crea una cuenta del personal. La contraseña se pide por teclado y solo se guarda su hash."

    def add_arguments(self, parser):
        parser.add_argument("--correo", required=True)
        parser.add_argument("--nombres", required=True)
        parser.add_argument("--apellidos", required=True)
        parser.add_argument("--rol", required=True, choices=Rol.values)
        parser.add_argument("--clinica-id", dest="clinica_id", help="Id de la clínica (24 caracteres hexadecimales)")
        parser.add_argument("--inactivo", action="store_true", help="Crea la cuenta desactivada")

    def handle(self, *args, **opciones):
        clinica_id = self._clinica_id(opciones["clinica_id"])
        contrasena = self._pedir_contrasena()

        try:
            validate_password(contrasena)
            administrador = Administrador.objects.create_user(
                correo=opciones["correo"],
                password=contrasena,
                nombres=opciones["nombres"],
                apellidos=opciones["apellidos"],
                rol=opciones["rol"],
                clinica_id=clinica_id,
                activo=not opciones["inactivo"],
            )
        except ValidationError as error:
            raise CommandError(" ".join(error.messages))

        estado = "inactiva" if opciones["inactivo"] else "activa"
        self.stdout.write(self.style.SUCCESS(
            f"Cuenta {estado} creada: {administrador.correo} · {administrador.get_rol_display()} · id {administrador.pk}"
        ))

    # Utilidades internas
    def _clinica_id(self, valor):
        if not valor:
            return None
        try:
            return ObjectId(valor)
        except InvalidId:
            raise CommandError("El id de la clínica debe tener 24 caracteres hexadecimales.")

    def _pedir_contrasena(self):
        contrasena = getpass.getpass("Contraseña: ")
        if contrasena != getpass.getpass("Repite la contraseña: "):
            raise CommandError("Las contraseñas no coinciden.")
        return contrasena