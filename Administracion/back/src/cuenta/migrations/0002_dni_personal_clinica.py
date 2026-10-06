from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("cuenta", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="administrador",
            name="dni",
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
    ]
