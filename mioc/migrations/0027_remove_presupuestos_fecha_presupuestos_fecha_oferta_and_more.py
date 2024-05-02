# Generated by Django 5.0.1 on 2024-03-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0026_alter_presupuestossubrubros_subrubro"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="presupuestos",
            name="fecha",
        ),
        migrations.AddField(
            model_name="presupuestos",
            name="fecha_oferta",
            field=models.DateField(null=True, verbose_name="Fecha Oferta"),
        ),
        migrations.AddField(
            model_name="presupuestos",
            name="fecha_presupuesto",
            field=models.DateField(null=True, verbose_name="Fecha Presupuesto"),
        ),
    ]