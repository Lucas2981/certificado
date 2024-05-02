# Generated by Django 5.0.1 on 2024-03-08 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0023_presupuestos_codpresupuesto"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="presupuestos",
            name="codPresupuesto",
        ),
        migrations.AddField(
            model_name="obras",
            name="codObra",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=200,
                null=True,
                verbose_name="Cod. Obra",
            ),
        ),
    ]