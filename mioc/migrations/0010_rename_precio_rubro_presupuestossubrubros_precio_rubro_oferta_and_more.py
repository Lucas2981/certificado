# Generated by Django 5.0.1 on 2024-03-04 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0009_alter_presupuestossubrubros_incidencias_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="presupuestossubrubros",
            old_name="precio_rubro",
            new_name="precio_rubro_oferta",
        ),
        migrations.RenameField(
            model_name="presupuestossubrubros",
            old_name="precio_total",
            new_name="precio_total_oferta",
        ),
        migrations.RenameField(
            model_name="presupuestossubrubros",
            old_name="precio_unitario",
            new_name="precio_unitario_presupuesto",
        ),
        migrations.AddField(
            model_name="presupuestossubrubros",
            name="precio_rubro_presupuesto",
            field=models.FloatField(
                blank=True, editable=False, null=True, verbose_name="Precio Rubro"
            ),
        ),
        migrations.AddField(
            model_name="presupuestossubrubros",
            name="precio_total_presupuesto",
            field=models.FloatField(
                blank=True, editable=False, null=True, verbose_name="Precio Total"
            ),
        ),
        migrations.AddField(
            model_name="presupuestossubrubros",
            name="precio_unitario_oferta",
            field=models.FloatField(
                default=0, editable=False, verbose_name="Precio Unitario"
            ),
            preserve_default=False,
        ),
    ]
