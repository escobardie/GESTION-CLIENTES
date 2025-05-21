from django.db import models
from apps.cliente.models import Cliente # Importamos el modelo Cliente desde la app cliente
from apps.ventas.models import Venta # Importamos el modelo Cliente desde la app cliente
from apps.promociones.models import Promo
from apps.usuarios.models import Usuario
import uuid


#################################
########## Modelo PAGO ##########
#################################
class Pagos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos_cliente', verbose_name='Usuario Asociado', null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente Asociada')
    venta = models.ForeignKey(Venta, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Venta Asociada')
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Promocion Asociada')
    monto = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Monto')
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Venta')
    metodo_pago = models.CharField(null=True, max_length=50, choices=[
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
    ])
    descripcion = models.TextField(null=True, blank=True, verbose_name='Nota') # Para detalles adicionales
    referencia = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Referencia de Pago"
    )

    token = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        editable=False,
        verbose_name="Token de acceso seguro"
    )


    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago de ${self.monto} por {self.usuario.username if self.usuario else '---'} el {self.fecha_pago.strftime('%Y-%m-%d')}"


    
