from django.db import models

###########################
#### Modelo PROMOCIONES ###
###########################

class Promo(models.Model):
    nombre_promo = models.CharField(max_length=250, verbose_name='Nombre Promo')
    valor_promo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio Promo')
    cant_bidones = models.PositiveIntegerField(verbose_name='Cantidad Bidones')  # Se cambia a PositiveIntegerField para garantizar valores positivos
    alta_promo = models.DateField(auto_now_add=True, verbose_name='Fecha Alta Promo')
    vencimiento_promo = models.DateField(verbose_name='Fecha Fin Promo')
    estado = models.BooleanField(default=True, verbose_name='Estado Promo')
    nota = models.TextField(null=True, blank=True, verbose_name='Nota')  # Hacemos que el campo "nota" sea opcional

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        ordering = ['-id']  # Ordenamos por las promociones más recientes primero
    
    def __str__(self):
        return f"{self.nombre_promo} - ${self.valor_promo}"
