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
    tipo_promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo de Promoción')
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
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
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




###########################
## Modelo REGISTRO PAGOS ##
###########################
class RegistroPago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Pago')
    # fecha = models.DateField(verbose_name='Fecha de Pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    comprobante = models.FileField(upload_to='comprobantes/registro_pagos/clientes', null=True, blank=True, verbose_name='Comprobante')
    nota = models.TextField(verbose_name='Nota')

    class Meta:
        verbose_name = 'Registro de Pago'
        verbose_name_plural = 'Registros de Pago'
        ordering = ['fecha']
    
    def __str__(self):
        return f"Pago de {self.cliente} el {self.fecha}"

