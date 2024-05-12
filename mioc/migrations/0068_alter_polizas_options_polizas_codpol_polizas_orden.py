# Generated by Django 5.0.1 on 2024-05-11 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0067_polizas_obra"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="polizas",
            options={
                "ordering": ["obra"],
                "verbose_name": "Poliza",
                "verbose_name_plural": "Polizas",
            },
        ),
        migrations.AddField(
            model_name="polizas",
            name="codPol",
            field=models.CharField(
                editable=False,
                max_length=200,
                null=True,
                unique=True,
                verbose_name="Cod. Poliza",
            ),
        ),
        migrations.AddField(
            model_name="polizas",
            name="orden",
            field=models.PositiveIntegerField(default=1, verbose_name="Nro Orden"),
        ),
    ]
