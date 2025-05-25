from django.contrib import admin
from . import models
from apps.cliente.admin import UsuarioConRolFilter # heredamos filtro 


class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre_producto', 'precio_producto', 'stock', 'estado')
    list_display = ('nombre_producto', 'precio_producto', 'stock', 'estado')
    list_filter = (UsuarioConRolFilter,)
    
admin.site.register(models.Producto, ProductoAdmin)
