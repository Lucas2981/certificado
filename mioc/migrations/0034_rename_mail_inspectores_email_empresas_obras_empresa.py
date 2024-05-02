# Generated by Django 5.0.1 on 2024-03-11 00:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0033_delete_ofertas"),
    ]

    operations = [
        migrations.RenameField(
            model_name="inspectores",
            old_name="mail",
            new_name="email",
        ),
        migrations.CreateModel(
            name="Empresas",
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
                ("name", models.CharField(max_length=200, verbose_name="Nombres")),
                (
                    "propietario",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Propietario",
                    ),
                ),
                (
                    "representante_tecnico",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Representante Técnico",
                    ),
                ),
                (
                    "calle",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Calle"
                    ),
                ),
                (
                    "telephone",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Teléfono"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="Correo"
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mioc.location",
                        verbose_name="Ubicación",
                    ),
                ),
            ],
            options={
                "verbose_name": "Empresa",
                "verbose_name_plural": "Empresas",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="obras",
            name="empresa",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mioc.empresas",
                verbose_name="Empresa",
            ),
        ),
    ]
