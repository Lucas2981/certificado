# Generated by Django 5.0.1 on 2024-03-09 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0027_remove_presupuestos_fecha_presupuestos_fecha_oferta_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="presupuestossubrubros",
            name="uvi_oferta",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mioc.uvis",
                verbose_name="Uvi",
            ),
        ),
    ]
