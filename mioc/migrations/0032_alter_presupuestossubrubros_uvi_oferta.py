# Generated by Django 5.0.1 on 2024-03-09 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0031_alter_presupuestossubrubros_incidencias_oferta_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="presupuestossubrubros",
            name="uvi_oferta",
            field=models.FloatField(
                blank=True, editable=False, null=True, verbose_name="Uvi"
            ),
        ),
    ]