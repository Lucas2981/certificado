# Generated by Django 5.0.1 on 2024-07-16 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0003_alter_certificadosaf_dispo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificadosaf",
            name="expediente",
            field=models.CharField(
                max_length=30, verbose_name="Expediente del certificado AF"
            ),
        ),
    ]