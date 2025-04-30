from django.db import models
from apps.cliente.models import Cliente # Importamos el modelo Cliente desde la app cliente
from apps.productos.models import Producto
from apps.usuarios.models import Usuario


##########################
###### Modelo VENTA ######
##########################
class Venta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas', verbose_name='Usuario Asociado', null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Venta')
    total_venta = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Total Venta')
    nota = models.TextField(null=True, blank=True, verbose_name='Nota')
    metodo_pago = models.CharField(null=True, max_length=50, choices=[
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
    ])

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta {self.id} - {self.fecha_venta}"

#################################
##### Modelo VENTA PRODUCTO #####
#################################
class VentaProducto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas_producto', verbose_name='Usuario Asociado', null=True)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Venta Producto')
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, verbose_name='Venta')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    descuento = models.PositiveIntegerField(default=0, verbose_name='Descuento')
    precio_unidad_venta = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Precio Venta')
    precio_total_venta = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Precio Total Venta')


    class Meta:
        unique_together = ('venta', 'producto')
        verbose_name='Venta por Producto'
        verbose_name_plural='Ventas por Producto'
        ordering = ['-id']

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.producto.precio_producto} - {self.cantidad} unidades - Total: {self.precio_total_venta:.2f}"

