# Generated by Django 5.1 on 2025-05-11 03:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suscripcion', '0004_pagosuscriptor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='suscripcionporusuario',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='suscripcion_asociada', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
