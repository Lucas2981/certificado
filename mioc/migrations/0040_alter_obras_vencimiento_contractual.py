# Generated by Django 5.0.1 on 2024-05-02 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0039_alter_obras_monto_uvi"),
    ]

    operations = [
        migrations.AlterField(
            model_name="obras",
            name="vencimiento_contractual",
            field=models.DateField(
                blank=True, null=True, verbose_name="Vencimiento Contractual"
            ),
        ),
    ]
