# Generated by Django 5.0.1 on 2024-07-09 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0014_obras_dispo_contrato"),
    ]

    operations = [
        migrations.AlterField(
            model_name="obras",
            name="dispo_contrato",
            field=models.CharField(
                max_length=30, unique=True, verbose_name="Dispo. Contrato"
            ),
        ),
        migrations.AlterField(
            model_name="obras",
            name="fecha_dispo",
            field=models.DateField(
                verbose_name="Fecha de dispo de Aceptación de Contrato"
            ),
        ),
    ]
