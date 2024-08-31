from django.contrib import admin
from . import models    


admin.site.site_header = 'Administración Clientes'
admin.site.index_title = 'Panel de Control'
admin.site.site_title = 'Cliente'


class ClientesAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre','apellido')
    list_display = ('nombre','apellido')

admin.site.register(models.Cliente, ClientesAdmin)

class PromoAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre_promo','valor_promo')
    list_display = ('nombre_promo','valor_promo')

admin.site.register(models.Promo, PromoAdmin)

class PromoPorClienteAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente_id','promo_id')
    list_display = ('cliente_id','promo_id')

admin.site.register(models.PromoPorCliente, PromoPorClienteAdmin)

class VisitaAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente_id','fecha_visita')
    list_display = ('cliente_id','fecha_visita')

admin.site.register(models.Visita, VisitaAdmin)

class RegsitroPagosAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha','cliente_id','monto')
    list_display = ('fecha','cliente_id','monto')

admin.site.register(models.RegistroPago, RegsitroPagosAdmin)