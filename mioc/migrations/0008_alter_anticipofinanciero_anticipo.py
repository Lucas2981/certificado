# Generated by Django 5.0.1 on 2024-07-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0007_alter_empresapoliza_telefono"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anticipofinanciero",
            name="anticipo",
            field=models.BooleanField(verbose_name="Anticipo"),
        ),
    ]
