# Generated by Django 5.0.1 on 2024-05-07 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0062_certificados_periodo_alter_certificados_fecha_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificados",
            name="periodo",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Periodo medido"
            ),
        ),
    ]