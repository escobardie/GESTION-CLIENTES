# Generated by Django 5.1 on 2024-11-18 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='metodo_pago',
            field=models.CharField(choices=[('tarjeta', 'Tarjeta de Crédito/Débito'), ('efectivo', 'Efectivo'), ('transferencia', 'Transferencia Bancaria')], max_length=50, null=True),
        ),
    ]