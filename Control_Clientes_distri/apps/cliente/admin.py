from django.contrib import admin
from . import models    


admin.site.site_header = 'Administración Clientes'
admin.site.index_title = 'Panel de Control'
admin.site.site_title = 'Cliente'


class ClientesAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre','apellido', 'direccion', 'telefono', 'fecha_alta', 'tipo_promo','fecha_cobro')
    list_display = ('nombre','apellido', 'direccion', 'tipo_promo','fecha_cobro')

admin.site.register(models.Cliente, ClientesAdmin)

class PromoAdmin(admin.ModelAdmin):
    readonly_fields = ('cant_bidones','nombre_promo')
    list_display = ('nombre_promo','cant_bidones','valor_promo')

admin.site.register(models.Promo, PromoAdmin)

class PromoPorClienteAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente','promo','inicio_promo','codigo_dispenser')
    list_display = ('cliente','promo','inicio_promo','estado')

admin.site.register(models.PromoPorCliente, PromoPorClienteAdmin)

class VisitaAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente','fecha_visita','nota')
    list_display = ('fecha_visita', 'cliente')

admin.site.register(models.Visita, VisitaAdmin)

class RegsitroPagosAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente','fecha','monto', 'comprobante', 'nota')
    list_display = ('fecha', 'cliente','monto')

admin.site.register(models.RegistroPago, RegsitroPagosAdmin)