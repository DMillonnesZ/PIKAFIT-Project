import django_mongodb_backend.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Clinica",
            fields=[
                ("id", django_mongodb_backend.fields.ObjectIdAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                )),
                ("razon_social", models.CharField(max_length=160)),
                ("ruc", models.CharField(max_length=11, unique=True)),
                ("direccion", models.CharField(max_length=255)),
                ("telefono", models.CharField(max_length=30)),
                ("activa", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "clinicas",
                "verbose_name": "clínica",
                "verbose_name_plural": "clínicas",
            },
        ),
    ]
