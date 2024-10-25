from django.contrib import admin
from . import models 


class VentaAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente', 'fecha_venta', 'total_venta', 'nota')
    list_display = ('cliente', 'fecha_venta')

admin.site.register(models.Venta, VentaAdmin)

class VentaProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'fecha', 'venta', 'producto', 'descuento', 'precio_unidad_venta', 'cantidad','precio_total_venta')
    list_display = ('id', 'fecha','venta', 'producto', 'cantidad','precio_total_venta')

admin.site.register(models.VentaProducto, VentaProductoAdmin)