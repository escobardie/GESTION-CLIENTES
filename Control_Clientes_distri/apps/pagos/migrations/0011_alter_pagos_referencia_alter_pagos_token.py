# Generated by Django 5.1 on 2025-05-17 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0010_alter_pagos_referencia_alter_pagos_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagos',
            name='referencia',
            field=models.CharField(editable=False, max_length=100, null=True, unique=True, verbose_name='Referencia de Pago'),
        ),
        migrations.AlterField(
            model_name='pagos',
            name='token',
            field=models.CharField(editable=False, max_length=64, null=True, unique=True, verbose_name='Token de acceso seguro'),
        ),
    ]
