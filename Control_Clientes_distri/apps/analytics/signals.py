from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.ventas.models import Venta
from apps.pagos.models import Pagos
from apps.cliente.models import Cliente
from apps.visitas.models import VisitaServis


# cuando se genera una venta o pago, se crea una notificacion
@receiver(post_save, sender=Venta)
# @receiver(post_save, sender=Pagos)
def notificar_dashboard(sender, instance, created, **kwargs):
    if created:
        print(f"📦 Señal: venta ID {instance.id} creada")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dashboard",
            {
                "type": "enviar_actualizacion",
                "data": {"msg": "nueva venta"},
            },
        )

# cuando se genera una pago, se crea una notificacion
# @receiver(post_save, sender=Venta)
@receiver(post_save, sender=Pagos)
def notificar_dashboard(sender, instance, created, **kwargs):
    if created:
        print(f"📦 Señal: pago ID {instance.id} creada")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dashboard",
            {
                "type": "enviar_actualizacion",
                "data": {"msg": "nueva venta"},
            },
        )


@receiver(post_save, sender=Cliente)
def notificar_dashboard(sender, instance, created, **kwargs):
    if created:
        print(f"📦 Señal: Cliente ID {instance.id} creado")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dashboard",
            {
                "type": "enviar_actualizacion",
                "data": {"msg": "nueva cliente"},
            },
        )

## TODO: VERIFICAR SI FALTAN GENERAR SEÑALES "VisitaServis" 

@receiver(post_save, sender=VisitaServis)
def notificar_dashboard(sender, instance, created, **kwargs):
    if created:
        print(f"📦 Señal: VisitaServis ID {instance.id} creado")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "dashboard",
            {
                "type": "enviar_actualizacion",
                "data": {"msg": "nueva cliente"},
            },
        )
