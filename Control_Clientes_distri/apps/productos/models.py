from django.db import models

###########################
##### Modelo PRODUCTO #####
###########################
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=250, verbose_name='Nombre Producto')
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    alta_producto = models.DateField(auto_now_add=True, verbose_name='Fecha Alta Producto')
    proveedor = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre Proveedor')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    imagen_url = models.ImageField(upload_to='productos/img', null=True, blank=True, verbose_name='Imagen URL', default='../static/post_default.png')
    # imagen_url = models.FileField(upload_to='productos/img', null=True, blank=True, verbose_name='Imagen URL')
    # FileField: Propósito: Se usa para subir y almacenar archivos en el servidor.
    descripcion_producto = models.TextField(null=True, blank=True, verbose_name='Descripcion')
    estado = models.BooleanField(default=True, verbose_name='Estado')

    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering = ['nombre_producto']

    def __str__(self):
        return f"{self.nombre_producto}"


