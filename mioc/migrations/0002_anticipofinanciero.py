# Generated by Django 5.0.1 on 2024-06-09 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AnticipoFinanciero",
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
                ("porcentaje", models.FloatField(verbose_name="Porcentaje")),
                (
                    "obra",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mioc.obras",
                        verbose_name="Obra",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Cargado por",
                    ),
                ),
            ],
            options={
                "verbose_name": "Anticipo financiero",
                "verbose_name_plural": "Anticipos financieros",
                "ordering": ["obra"],
            },
        ),
    ]
