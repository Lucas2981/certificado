# Generated by Django 5.0.1 on 2024-03-06 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0018_alter_presupuestossubrubros_precio_total_oferta_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Unidades",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Unidad")),
            ],
            options={
                "verbose_name": "Unidad",
                "verbose_name_plural": "Unidades",
                "ordering": ["name"],
            },
        ),
        migrations.AlterField(
            model_name="presupuestossubrubros",
            name="incidencias_presupuesto",
            field=models.FloatField(blank=True, null=True, verbose_name="Incidencias"),
        ),
        migrations.AddField(
            model_name="subrubros",
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
