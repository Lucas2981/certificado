# Generated by Django 5.0.1 on 2024-07-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0006_alter_empresapoliza_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="empresapoliza",
            name="telefono",
            field=models.CharField(
                blank=True, max_length=11, null=True, verbose_name="Teléfono"
            ),
        ),
    ]