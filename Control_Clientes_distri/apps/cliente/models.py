from django.db import models
from apps.promociones.models import Promo



###########################
###### Modelo CLIENTE #####
###########################
class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    apellido = models.CharField(max_length=150, verbose_name='Apellido')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    direccion = models.CharField(max_length=150, verbose_name='Dirección')
    fecha_alta = models.DateField(auto_now_add=True, verbose_name='Fecha de Alta')
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
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Promoción')
    inicio_promo = models.DateTimeField(auto_now_add=True, verbose_name='Inicio de Promo')
    fin_promo = models.DateField(verbose_name='Fin de Promo')
    fecha_pago_promo = models.DateField(null=True, blank=True, verbose_name='Fecha de Pago Promo')
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

