from rest_framework.permissions import BasePermission


class EsAdministradorGimnasio(BasePermission):
    message = "Solo el administrador del gimnasio puede modificar este catálogo."

    def has_permission(self, request, view):
        usuario = request.user
        return bool(
            usuario
            and usuario.is_authenticated
            and getattr(usuario, "rol", None) == "administrador_gimnasio"
        )
