# Generated by Django 5.0.1 on 2024-06-02 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0003_certificados_creado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificados",
            name="avance_acum_med",
            field=models.FloatField(
                default=0, verbose_name="Avance real acumulado (%)"
            ),
        ),
        migrations.AlterField(
            model_name="certificados",
            name="avance_acum_proy",
            field=models.FloatField(
                default=0, verbose_name="Avance proyectado acumulado (%)"
            ),
        ),
    ]