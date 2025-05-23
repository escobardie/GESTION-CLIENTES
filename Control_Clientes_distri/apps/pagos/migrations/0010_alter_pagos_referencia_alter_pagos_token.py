# Generated by Django 5.1 on 2025-05-17 01:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0009_auto_20250517_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagos',
            name='referencia',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, unique=True, verbose_name='Referencia de Pago'),
        ),
        migrations.AlterField(
            model_name='pagos',
            name='token',
            field=models.CharField(editable=False, max_length=64, unique=True, verbose_name='Token de acceso seguro'),
        ),
    ]
