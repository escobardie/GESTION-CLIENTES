# Generated by Django 5.1 on 2025-05-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='codigo_area',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Código de Área'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='latitud',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Latitud'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='localidad',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Localidad'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='longitud',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Longitud'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='observacion',
            field=models.TextField(blank=True, null=True, verbose_name='Observación'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='provincia',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Provincia'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='ubicacion',
            field=models.TextField(blank=True, null=True, verbose_name='Ubicación'),
        ),
        migrations.AlterField(
            model_name='promoporcliente',
            name='codigo_dispenser',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Código Dispenser'),
        ),
        migrations.AlterField(
            model_name='promoporcliente',
            name='nota',
            field=models.TextField(blank=True, null=True, verbose_name='Nota'),
        ),
    ]
