from django.contrib import admin
from . import models
from apps.cliente.admin import UsuarioConRolFilter # heredamos filtro 


class PagoAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_pago', 'venta', 'promo','cliente', 'monto','metodo_pago', 'descripcion')
    list_display = ('fecha_pago', 'cliente', 'monto','metodo_pago', 'descripcion')
    list_filter = (UsuarioConRolFilter,)

admin.site.register(models.Pagos, PagoAdmin)