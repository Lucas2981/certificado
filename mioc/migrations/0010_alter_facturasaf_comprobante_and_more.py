# Generated by Django 5.0.1 on 2024-07-16 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0009_facturasaf"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facturasaf",
            name="comprobante",
            field=models.PositiveIntegerField(verbose_name="Comprobante N°"),
        ),
        migrations.AlterField(
            model_name="facturasaf",
            name="pto_venta",
            field=models.PositiveIntegerField(verbose_name="Punto de Venta N°"),
        ),
    ]
