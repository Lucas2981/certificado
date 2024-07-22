# Generated by Django 5.0.1 on 2024-07-16 22:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0008_dispocertaf_observacion"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="facturasAF",
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
                    "tipo",
                    models.CharField(
                        choices=[(0, "A"), (1, "B"), (2, "C")],
                        max_length=30,
                        verbose_name="Tipo",
                    ),
                ),
                (
                    "pto_venta",
                    models.PositiveIntegerField(
                        max_length=4, verbose_name="Punto de Venta N°"
                    ),
                ),
                (
                    "comprobante",
                    models.PositiveIntegerField(
                        max_length=10, verbose_name="Comprobante N°"
                    ),
                ),
                ("fecha", models.DateField(verbose_name="Fecha Emisión")),
                ("cuit", models.CharField(max_length=30, verbose_name="CUIT Empresa")),
                ("monto", models.FloatField(verbose_name="Importe Total")),
                (
                    "certificado",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mioc.certificadosaf",
                        verbose_name="Certificado",
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
                "verbose_name": "Factura Certificado AF",
                "verbose_name_plural": "Facturas Certificados AF",
                "ordering": ["-fecha"],
            },
        ),
    ]