from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.ventas.models import Venta
from apps.pagos.models import Pagos


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


# @receiver(post_save, sender=Venta)
# def notificar_nueva_venta(sender, instance, created, **kwargs):
#     if created:
#         print("Entro una analytics/signals.py notificar_nueva_venta")
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "dashboard",
#             {
#                 "type": "enviar_actualizacion",
#                 "data": {
#                     "venta_id": instance.id,
#                     "total": instance.total_venta,
#                     "cliente": str(instance.cliente),
#                     "fecha": instance.fecha_venta.strftime("%Y-%m-%d %H:%M"),
#                 },
#             },
#         )
