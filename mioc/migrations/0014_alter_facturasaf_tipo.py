# Generated by Django 5.0.1 on 2024-07-18 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0013_alter_facturasaf_tipo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facturasaf",
            name="tipo",
            field=models.CharField(
                choices=[("0", "A"), ("1", "B"), ("2", "C")],
                default="1",
                max_length=1,
                verbose_name="Tipo",
            ),
        ),
    ]