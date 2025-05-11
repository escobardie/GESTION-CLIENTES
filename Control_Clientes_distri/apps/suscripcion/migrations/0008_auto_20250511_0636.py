from django.db import migrations
import uuid

def generar_tokens(apps, schema_editor):
    Pago = apps.get_model('suscripcion', 'PagoSuscriptor')
    for pago in Pago.objects.filter(token__isnull=True):
        pago.token = uuid.uuid4().hex
        pago.save()

class Migration(migrations.Migration):

    dependencies = [
        ('suscripcion', '0007_pagosuscriptor_token_alter_pagosuscriptor_referencia'),
    ]

    operations = [
        migrations.RunPython(generar_tokens),
    ]
