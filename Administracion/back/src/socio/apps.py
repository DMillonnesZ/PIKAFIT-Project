from django.apps import AppConfig


class SocioConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "socio"
