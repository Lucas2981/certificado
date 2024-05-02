# Generated by Django 5.0.1 on 2024-03-06 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0019_unidades_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="presupuestossubrubros",
            name="unidad",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mioc.unidades",
                verbose_name="Unidad",
            ),
        ),
    ]