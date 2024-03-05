# Generated by Django 5.0.1 on 2024-03-04 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0008_alter_presupuestossubrubros_cantidad_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="presupuestossubrubros",
            name="incidencias",
            field=models.FloatField(
                blank=True, editable=False, null=True, verbose_name="Incidencias"
            ),
        ),
        migrations.AlterField(
            model_name="presupuestossubrubros",
            name="precio_rubro",
            field=models.FloatField(
                blank=True, editable=False, null=True, verbose_name="Precio Rubro"
            ),
        ),
        migrations.AlterField(
            model_name="presupuestossubrubros",
            name="precio_total",
            field=models.FloatField(
                blank=True, editable=False, null=True, verbose_name="Precio Total"
            ),
        ),
    ]