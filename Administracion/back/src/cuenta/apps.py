from django.apps import AppConfig


class CuentaConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "cuenta"
    verbose_name = "Cuentas del personal"