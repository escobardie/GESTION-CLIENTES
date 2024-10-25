from django.contrib import admin
from . import models 

# Register your models here.
class PagoAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_pago', 'venta', 'promo','cliente', 'monto','metodo_pago', 'descripcion')
    list_display = ('fecha_pago', 'cliente', 'monto','metodo_pago', 'descripcion')

admin.site.register(models.Pagos, PagoAdmin)