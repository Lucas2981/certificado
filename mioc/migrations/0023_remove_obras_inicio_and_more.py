# Generated by Django 5.0.1 on 2024-07-20 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mioc", "0022_alter_plantrabajo_uvisacumesperados_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="obras",
            name="inicio",
        ),
        migrations.RemoveField(
            model_name="obras",
            name="vencimiento_contractual",
        ),
        migrations.AddField(
            model_name="actasinicio",
            name="vencimiento_contractual",
            field=models.DateField(
                blank=True,
                editable=False,
                null=True,
                verbose_name="Vencimiento Contractual",
            ),
        ),
    ]
