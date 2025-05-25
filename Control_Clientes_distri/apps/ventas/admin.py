from django.contrib import admin
from . import models 
from apps.cliente.admin import UsuarioConRolFilter # heredamos filtro 


class VentaAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente', 'fecha_venta', 'total_venta','metodo_pago', 'nota')
    list_display = ('cliente', 'fecha_venta','metodo_pago')
    list_filter = (UsuarioConRolFilter,)

admin.site.register(models.Venta, VentaAdmin)

class VentaProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'fecha', 'venta', 'producto', 'descuento', 'precio_unidad_venta', 'cantidad','precio_total_venta')
    list_display = ('id', 'fecha','venta', 'producto', 'cantidad','precio_total_venta')
    list_filter = (UsuarioConRolFilter,)
    
admin.site.register(models.VentaProducto, VentaProductoAdmin)