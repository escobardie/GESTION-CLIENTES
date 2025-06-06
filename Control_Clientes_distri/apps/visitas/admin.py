from django.contrib import admin
from . import models
from apps.cliente.admin import UsuarioConRolFilter # heredamos filtro 


class VisitaAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente','fecha_visita','nota')
    list_display = ('fecha_visita', 'cliente')
    list_filter = (UsuarioConRolFilter,)

admin.site.register(models.Visita, VisitaAdmin)

class VisitaServisAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario','cliente','nombre_promocion','b_disponible','b_entregado','b_retirado','b_en_poder_clte','fecha_visita','nota')
    list_display = ('fecha_visita', 'cliente')
    list_filter = (UsuarioConRolFilter,)

admin.site.register(models.VisitaServis, VisitaServisAdmin)