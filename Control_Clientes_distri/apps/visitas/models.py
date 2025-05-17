from django.db import models
from apps.cliente.models import Cliente # Importamos el modelo Cliente desde la app cliente
from apps.usuarios.models import Usuario
import uuid


###########################
###### Modelo VISITAS #####
###########################
class Visita(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='visita_cliente', verbose_name='Usuario Asociado', null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    fecha_visita = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Visita')
    referencia = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        default=uuid.uuid4,  
        verbose_name="Referencia de Visita"
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        null=False,  
        editable=False,
        verbose_name="Token de acceso seguro"
    )
    nota = models.TextField(verbose_name='Nota')

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-fecha_visita']
    
    def __str__(self):
        return f"Visita a {self.cliente} el {self.fecha_visita.strftime('%d/%m/%Y %H:%M')}"


class VisitaServis(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='visita_servis_cliente', verbose_name='Usuario Asociado', null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    fecha_visita = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Visita')
    nombre_promocion = models.CharField(max_length=250, verbose_name='Nombre Promoción')
    b_disponible = models.IntegerField(default=0, verbose_name='Bidones Disponibles')
    b_entregado = models.IntegerField(default=0, verbose_name='Bidones Entregados')
    b_retirado = models.IntegerField(default=0, verbose_name='Bidondes retirados')
    b_en_poder_clte = models.IntegerField(default=0, verbose_name='Bidones en poder del cliente')    
    referencia = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        default=uuid.uuid4,  
        verbose_name="Referencia de Visita"
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        null=False,  
        editable=False,
        verbose_name="Token de acceso seguro"
    )
    nota = models.TextField(null=True, blank=True, verbose_name='Nota u Observación')



    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Visita Servicio'
        verbose_name_plural = 'Visitas Servicios'
        ordering = ['-fecha_visita']

    def __str__(self):
        return f"Visita a {self.cliente} con promo {self.nombre_promocion} el {self.fecha_visita.strftime('%d/%m/%Y %H:%M')}"