from django.db import models
import uuid
from apps.usuarios.models import Usuario

def generar_token():
    import uuid
    return uuid.uuid4().hex



class Suscripcion(models.Model):
    nombre_suscripcion = models.CharField(max_length=250, verbose_name='Nombre Suscripción')
    valor_suscripcion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Suscripción')
    fecha_alta = models.DateField(auto_now_add=True, verbose_name='Fecha Alta Suscripción')
    # fecha_cobro = models.DateField(verbose_name='Fecha Cobro')
    fecha_vencimiento = models.DateField(verbose_name='Fecha Vencimiento')
    # Opciones de suscripción
    COBRO_OPCIONES = [
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    tipo_cobro_suscrip = models.CharField(default='mensual',max_length=10, choices=COBRO_OPCIONES, verbose_name='Tipo de Suscripción')
    limite_clientes = models.IntegerField(default=0, verbose_name='Límite de Clientes')
    limite_empleados = models.IntegerField(default=0, verbose_name='Límite de Empleados')
    estado = models.BooleanField(default=True, verbose_name='Estado Suscripción')
    nota = models.TextField(null=True, blank=True, verbose_name='Nota')  # Hacemos que el campo "nota" sea opcional


    class Meta:
        verbose_name = 'Suscripción'
        verbose_name_plural = 'Suscripciones'
        ordering = ['-id']  # Ordenamos por las Suscripciones más recientes primero
    
    def __str__(self):
        return f"{self.nombre_suscripcion} - ${self.valor_suscripcion}"
    


class SuscripcionPorUsuario(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='suscripcion_asociada',
        verbose_name='Usuario'
    )
    suscripcion = models.ForeignKey(
        Suscripcion,
        on_delete=models.CASCADE,
        related_name='usuarios_asociados',
        verbose_name='Suscripción'
    )
    fecha_asignacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Asignación')
    fecha_cobro_suscrip = models.DateField(verbose_name='Fecha Cobro Suscripción')
    fecha_fin_suscrip = models.DateField(verbose_name='Fin de Suscripción')

    estado = models.BooleanField(default=True, verbose_name='Estado')
    nota = models.TextField(verbose_name='Nota')

    class Meta:
        verbose_name = 'Suscripción por Usuario'
        verbose_name_plural = 'Suscripciones por Usuario'

    def __str__(self):
        return f"{self.usuario.username} → {self.suscripcion.nombre_suscripcion}"

class PagoSuscriptor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos_suscrip_usuario', verbose_name='Usuario Asociado', null=True)
    suscripcion = models.ForeignKey(Suscripcion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Suscripcion Asociada')
    monto = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Monto')
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Pago')
    metodo_pago = models.CharField(
        max_length=50,
        choices=[
            ('tarjeta', 'Tarjeta de Crédito/Débito'),
            ('efectivo', 'Efectivo'),
            ('transferencia', 'Transferencia Bancaria'),
        ],
        null=True,
        blank=True,
        verbose_name='Método de Pago'
    )
    estado_pago = models.CharField(
        max_length=20,
        choices=[('completado', 'Completado'), ('pendiente', 'Pendiente'), ('fallido', 'Fallido')],
        default='completado',
        verbose_name='Estado del Pago'
    )
    descripcion = models.TextField(null=True, blank=True, verbose_name='Nota') # Para detalles adicionales
    referencia = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        default=uuid.uuid4,  
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
        verbose_name = 'Pago Suscripción'
        verbose_name_plural = 'Pagos Suscripciones'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"Pago de {self.monto} el {self.fecha_pago.strftime('%Y-%m-%d')}"