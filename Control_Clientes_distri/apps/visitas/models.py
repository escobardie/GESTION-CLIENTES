from django.db import models
from apps.cliente.models import Cliente # Importamos el modelo Cliente desde la app cliente
from apps.usuarios.models import Usuario


###########################
###### Modelo VISITAS #####
###########################
class Visita(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='visita_cliente', verbose_name='Usuario Asociado', null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cliente')
    fecha_visita = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Visita')
    nota = models.TextField(verbose_name='Nota')

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-fecha_visita']
    
    def __str__(self):
        return f"Visita a {self.cliente} el {self.fecha_visita.strftime('%d/%m/%Y %H:%M')}"

