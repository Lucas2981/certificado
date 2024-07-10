# Generated by Django 5.0.1 on 2024-07-07 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="inspectores",
            options={
                "ordering": ["fullname"],
                "verbose_name": "Inspector",
                "verbose_name_plural": "Inspectores",
            },
        ),
        migrations.AlterField(
            model_name="actasinicio",
            name="fecha",
            field=models.DateField(verbose_name="Fecha de inicio"),
        ),
    ]
