# Generated by Django 5.1 on 2024-09-18 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0007_alter_ventaproducto_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen_url',
            field=models.ImageField(blank=True, default='../static/post_default.png', null=True, upload_to='productos/img', verbose_name='Imagen URL'),
        ),
    ]
