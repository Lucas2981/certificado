# Generated by Django 5.0.1 on 2024-05-12 22:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0069_polizas_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="polizas",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Creada por",
            ),
        ),
        migrations.CreateModel(
            name="Memorias",
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
                    "memoria",
                    models.TextField(blank=True, null=True, verbose_name="Memoria"),
                ),
                (
                    "resumen",
                    models.TextField(blank=True, null=True, verbose_name="Resumen"),
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
            options={
                "verbose_name": "Memoria",
                "verbose_name_plural": "Memorias",
                "ordering": ["obra"],
            },
        ),
    ]
