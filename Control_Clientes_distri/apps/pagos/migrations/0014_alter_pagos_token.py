# Generated by Django 5.1 on 2025-05-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0013_alter_pagos_referencia_alter_pagos_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagos',
            name='token',
            field=models.CharField(default='4f3e75a8107a411ba1264a1f9cc481b7', editable=False, max_length=64, unique=True, verbose_name='Token de acceso seguro'),
        ),
    ]
