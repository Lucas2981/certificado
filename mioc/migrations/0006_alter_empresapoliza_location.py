# Generated by Django 5.0.1 on 2024-07-08 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0005_alter_empresapoliza_cuit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="empresapoliza",
            name="location",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Domicilio"
            ),
        ),
    ]