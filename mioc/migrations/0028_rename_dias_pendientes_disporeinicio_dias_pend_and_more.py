# Generated by Django 5.0.1 on 2024-07-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0027_disporeinicio"),
    ]

    operations = [
        migrations.RenameField(
            model_name="disporeinicio",
            old_name="dias_pendientes",
            new_name="dias_pend",
        ),
        migrations.RenameField(
            model_name="disporeinicio",
            old_name="nueva_vencimiento",
            new_name="nuevo_vencimiento",
        ),
        migrations.AddField(
            model_name="disporeinicio",
            name="dias_pend_acum",
            field=models.IntegerField(
                default=0, verbose_name="Días pendientes acumulados"
            ),
        ),
    ]
