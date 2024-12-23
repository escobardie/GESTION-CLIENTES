# Generated by Django 5.1 on 2024-10-13 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0016_remove_ventaproducto_producto_and_more'),
        ('promociones', '0001_initial'),
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Monto')),
                ('fecha_pago', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Venta')),
                ('metodo_pago', models.CharField(choices=[('tarjeta', 'Tarjeta de Crédito/Débito'), ('efectivo', 'Efectivo'), ('transferencia', 'Transferencia Bancaria')], max_length=50, null=True)),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Nota')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cliente.cliente', verbose_name='Cliente Asociada')),
                ('promo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='promociones.promo', verbose_name='Promocion Asociada')),
                ('venta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ventas.venta', verbose_name='Venta Asociada')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
                'ordering': ['-fecha_pago'],
            },
        ),
    ]
