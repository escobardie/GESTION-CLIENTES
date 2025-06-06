# Generated by Django 5.1 on 2025-04-29 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=250, verbose_name='Nombre Producto')),
                ('precio_producto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('alta_producto', models.DateField(auto_now_add=True, verbose_name='Fecha Alta Producto')),
                ('proveedor', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre Proveedor')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('imagen_url', models.ImageField(blank=True, default='../static/post_default.png', null=True, upload_to='productos/img', verbose_name='Imagen URL')),
                ('descripcion_producto', models.TextField(blank=True, null=True, verbose_name='Descripcion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['nombre_producto'],
            },
        ),
    ]
