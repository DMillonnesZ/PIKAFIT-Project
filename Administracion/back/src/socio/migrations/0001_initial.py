import django_mongodb_backend.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Plan",
            fields=[
                ("id", django_mongodb_backend.fields.ObjectIdAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("duracion_dias", models.PositiveIntegerField()),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10)),
                ("activo", models.BooleanField(default=True)),
            ],
            options={"db_table": "planes", "ordering": ["nombre"]},
        ),
        migrations.CreateModel(
            name="Socio",
            fields=[
                ("id", django_mongodb_backend.fields.ObjectIdAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombres", models.CharField(max_length=100)),
                ("apellidos", models.CharField(max_length=120)),
                ("dni", models.CharField(max_length=8, unique=True)),
                ("correo", models.EmailField(max_length=254, unique=True)),
                ("sede_id", django_mongodb_backend.fields.ObjectIdField()),
                ("activo", models.BooleanField(default=True)),
            ],
            options={"db_table": "socios", "ordering": ["apellidos", "nombres"]},
        ),
        migrations.CreateModel(
            name="Membresia",
            fields=[
                ("id", django_mongodb_backend.fields.ObjectIdAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("socio_id", django_mongodb_backend.fields.ObjectIdField()),
                ("plan_id", django_mongodb_backend.fields.ObjectIdField()),
                ("fecha_inicio", models.DateField()),
                ("fecha_fin", models.DateField()),
                ("activa", models.BooleanField(default=True)),
            ],
            options={"db_table": "membresias", "ordering": ["-fecha_fin"]},
        ),
    ]
