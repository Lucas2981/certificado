# Generated by Django 5.0.1 on 2024-07-21 14:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0024_remove_obras_plazo_obras_plazonro_obras_plazotipo"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DispoParalizacion",
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
                    "fecha_paralizacion",
                    models.DateField(verbose_name="Fecha de paralización"),
                ),
                (
                    "dispo_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mioc.dispo_plan_trabajo",
                        verbose_name="Disposición de Plan de Trabajo",
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
                "verbose_name": "Disposición de paralización",
                "verbose_name_plural": "Disposiciones de paralización",
                "ordering": ["dispo_plan", "fecha_paralizacion"],
            },
        ),
        migrations.DeleteModel(
            name="ActasObras",
        ),
        migrations.DeleteModel(
            name="ActaTipo",
        ),
    ]
