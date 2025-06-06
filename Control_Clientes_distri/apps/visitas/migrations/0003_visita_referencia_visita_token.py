# Generated by Django 5.1 on 2025-05-15 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitas', '0002_visitaservis'),
    ]

    operations = [
        migrations.AddField(
            model_name='visita',
            name='referencia',
            field=models.CharField(default=True, editable=False, max_length=100, unique=True, verbose_name='Referencia de Visita'),
        ),
        migrations.AddField(
            model_name='visita',
            name='token',
            field=models.CharField(editable=False, max_length=64, null=True, unique=True, verbose_name='Token de acceso seguro'),
        ),
    ]
