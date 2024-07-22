# Generated by Django 5.0.1 on 2024-07-20 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0018_dispo_plan_trabajo_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlanTrabajo",
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
                ("periodoNro", models.PositiveIntegerField(verbose_name="Periodo N°")),
                ("fechaPeriodo", models.DateField(verbose_name="Fecha del Periodo")),
                (
                    "uvisEsperados",
                    models.PositiveIntegerField(verbose_name="UVIS Esperados"),
                ),
                (
                    "uvisAcumEsperados",
                    models.PositiveIntegerField(verbose_name="UVIS Acum. Esperados"),
                ),
                (
                    "dispo_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mioc.dispo_plan_trabajo",
                        verbose_name="Dispo. Plan de Trabajo",
                    ),
                ),
            ],
            options={
                "verbose_name": "Plan de Trabajo",
                "verbose_name_plural": "Planes de Trabajo",
                "ordering": ["dispo_plan", "periodoNro"],
            },
        ),
    ]