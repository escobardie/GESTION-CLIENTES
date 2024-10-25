from django.contrib import admin
from . import models 

class PromoAdmin(admin.ModelAdmin):
    readonly_fields = ('cant_bidones','nombre_promo')
    list_display = ('nombre_promo','cant_bidones','valor_promo')

admin.site.register(models.Promo, PromoAdmin)