# Generated by Django 5.0.1 on 2024-07-09 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0012_alter_anticipofinanciero_anticipo"),
    ]

    operations = [
        migrations.AddField(
            model_name="obras",
            name="fecha_dispo",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Fecha de dispo de Aceptación de Contrato",
            ),
        ),
    ]