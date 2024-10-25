from django.contrib import admin
from . import models 

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre_producto', 'precio_producto', 'stock', 'estado')
    list_display = ('nombre_producto', 'precio_producto', 'stock', 'estado')

admin.site.register(models.Producto, ProductoAdmin)
