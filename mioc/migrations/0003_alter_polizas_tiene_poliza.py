# Generated by Django 5.0.1 on 2024-07-08 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0002_alter_inspectores_options_alter_actasinicio_fecha"),
    ]

    operations = [
        migrations.AlterField(
            model_name="polizas",
            name="tiene_poliza",
            field=models.BooleanField(verbose_name="Presenta póliza de sustitución?"),
        ),
    ]