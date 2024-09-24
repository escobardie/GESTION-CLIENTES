from django.db import models

# Create your models here.

###########################
#### Modelo PROMOCIONES ###
###########################

class Promo(models.Model):
    nombre_promo = models.CharField(max_length=250, verbose_name='Nombre Promo')
    valor_promo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Promo')
    cant_bidones = models.IntegerField(verbose_name='Cantidad Bidones')
    alta_promo = models.DateField(auto_now_add=True, verbose_name='Fecha Alta Promo')
    vencimiento_promo = models.DateField(verbose_name='Fecha Fin Promo')
    estado = models.BooleanField(default=True, verbose_name='Estado Promo')
    nota = models.TextField(verbose_name='Nota')

    class Meta:
        verbose_name='Promoción'
        verbose_name_plural='Promociones'
        ordering = ['id']
    
    def __str__(self):
        return self.nombre_promo


###########################
###### Modelo CLIENTE #####
###########################
class Cliente(models.Model):
    # SE ELIMINAR LA REALACION, YA QUE ESTA MAS CREADA
    # tipo_promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo de Promoción')
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    apellido = models.CharField(max_length=150, verbose_name='Apellido')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    direccion = models.CharField(max_length=150, verbose_name='Dirección')
    fecha_alta = models.DateField(auto_now_add=True, verbose_name='Fecha de Alta')
    fecha_cobro = models.DateField(verbose_name='Fecha de Cobro')
    estado = models.BooleanField(default=True, verbose_name='Estado')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


############################
# Modelo PROMOCION * CLTE  #
############################
class PromoPorCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente', related_name='promociones')
    # cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente') # ORIGINAL
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Promoción')
    inicio_promo = models.DateTimeField(auto_now_add=True, verbose_name='Inicio de Promo')
    # inicio_promo = models.DateField(verbose_name='Inicio de Promo')
    fin_promo = models.DateField(verbose_name='Fin de Promo')
    ########## control de bidones ##########
    bidones_disponibles = models.IntegerField(verbose_name='Bidones Disponibles')
    entrega_bidones = models.IntegerField(default=0, verbose_name='Entrega de Bidones')
    retorno_bidones = models.IntegerField(default=0, verbose_name='Retorno de Bidones')
    bidones_acumulados = models.IntegerField(default=0, verbose_name='Bidones Acumulados')
    ########## control de bidones ##########
    codigo_dispenser = models.CharField(max_length=20, verbose_name='Código Dispenser')
    estado = models.BooleanField(default=True, verbose_name='Estado')
    nota = models.TextField(verbose_name='Nota')

    class Meta:
        verbose_name = 'Promoción por Cliente'
        verbose_name_plural = 'Promociones por Cliente'
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.cliente} - {self.promo}"




###########################
###### Modelo VISITAS #####
###########################
class Visita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    # fecha_visita = models.DateField(auto_now_add=True, verbose_name='Fecha de Visita')
    fecha_visita = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Visita')
    nota = models.TextField(verbose_name='Nota')

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['fecha_visita']
    
    def __str__(self):
        return f"Visita a {self.cliente} el {self.fecha_visita.strftime('%d/%m/%Y %H:%M')}"



##########################
###### Modelo VENTA ######
##########################
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Venta')

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta {self.id} - {self.fecha_venta}"


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
        return f"Producto {self.nombre_producto} ${self.precio_producto}"




#################################
##### Modelo VENTA PRODUCTO #####
#################################
class VentaProducto(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Venta Producto')
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, verbose_name='Venta')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    descuento = models.PositiveIntegerField(default=0, verbose_name='Descuento')
    precio_unidad_venta = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Precio Venta')
    # precio_venta: almacenan el precio de venta individual del producto.
    # tambien puede estar alacenando el precio ya con el descuento aplicado
    precio_total_venta = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Precio Total Venta')

    # # Se calcula el total, no es necesario almacenar un campo derivado
    # @property
    # def precio_total_venta(self):
    #     return (self.precio_unidad_venta * self.cantidad) - self.descuento

    class Meta:
        unique_together = ('venta', 'producto')
        verbose_name='Venta por Producto'
        verbose_name_plural='Ventas por Producto'
        ordering = ['-id']

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.producto.precio_producto} - {self.cantidad} unidades - Total: {self.precio_total_venta:.2f}"