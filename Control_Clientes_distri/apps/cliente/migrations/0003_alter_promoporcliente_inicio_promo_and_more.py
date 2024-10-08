# Generated by Django 5.1 on 2024-09-08 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_promoporcliente_bidones_acumulados_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promoporcliente',
            name='inicio_promo',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Visita'),
        ),
        migrations.AlterField(
            model_name='registropago',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Pago'),
        ),
        migrations.AlterField(
            model_name='visita',
            name='fecha_visita',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Visita'),
        ),
    ]
