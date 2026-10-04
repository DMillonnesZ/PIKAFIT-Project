import django_mongodb_backend.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sede",
            fields=[
                ("id", django_mongodb_backend.fields.ObjectIdAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                )),
                ("nombre", models.CharField(max_length=120)),
                ("direccion", models.CharField(max_length=255)),
                ("activa", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "sedes",
                "verbose_name": "sede",
                "verbose_name_plural": "sedes",
            },
        ),
    ]
