import django_mongodb_backend.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Maquina",
            fields=[
                ("id", django_mongodb_backend.fields.ObjectIdAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                )),
                ("codigo", models.CharField(max_length=40, unique=True)),
                ("nombre", models.CharField(max_length=120)),
                ("numero_serie", models.CharField(max_length=80, unique=True)),
                ("grupo_muscular", models.CharField(max_length=80)),
                ("sede_id", django_mongodb_backend.fields.ObjectIdField()),
                ("estado", models.CharField(choices=[("operativa", "Operativa"), ("mantenimiento", "En mantenimiento"), ("fuera_servicio", "Fuera de servicio")], max_length=20)),
                ("token_qr", models.CharField(editable=False, max_length=32, unique=True)),
            ],
            options={"db_table": "maquinas", "ordering": ["codigo"]},
        ),
    ]
