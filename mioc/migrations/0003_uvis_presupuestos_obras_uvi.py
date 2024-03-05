# Generated by Django 5.0.1 on 2024-03-04 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0002_alter_obras_vencimiento_ampliacion_1_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Uvis",
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
                (
                    "fecha",
                    models.DateField(blank=True, null=True, verbose_name="Fecha"),
                ),
                (
                    "valor",
                    models.FloatField(blank=True, null=True, verbose_name="Valor"),
                ),
            ],
            options={
                "verbose_name": "Uvi",
                "verbose_name_plural": "Uvis",
                "ordering": ["fecha"],
            },
        ),
        migrations.CreateModel(
            name="Presupuestos",
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
                (
                    "obra",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mioc.obras",
                        verbose_name="Obra",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="obras",
            name="uvi",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mioc.uvis",
                verbose_name="Uvi",
            ),
        ),
    ]
