from django.contrib import admin
from . import models
from apps.cliente.admin import UsuarioConRolFilter # heredamos filtro 


class PromoAdmin(admin.ModelAdmin):
    readonly_fields = ('cant_bidones','nombre_promo')
    list_display = ('nombre_promo','cant_bidones','valor_promo')
    list_filter = (UsuarioConRolFilter,)

admin.site.register(models.Promo, PromoAdmin)