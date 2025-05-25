from django.contrib import admin
from . import models
from django.utils.html import format_html
from apps.usuarios.models import Usuario

admin.site.site_header = 'Administración Clientes'
admin.site.index_title = 'Panel de Control'
admin.site.site_title = 'Cliente'

class UsuarioConRolFilter(admin.SimpleListFilter):
    title = 'Usuario (rol=usuario)'  # Texto que aparece en el filtro lateral
    parameter_name = 'usuario'

    def lookups(self, request, model_admin):
        # Lista de usuarios con rol = 'usuario'
        usuarios = Usuario.objects.filter(rol='usuario')
        return [(u.id, u.username) for u in usuarios]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(usuario__id=self.value())
        return queryset


class ClientesAdmin(admin.ModelAdmin):
    readonly_fields = ('nombre', 'apellido', 'direccion', 'telefono', 'fecha_alta')
    list_display = ('nombre', 'apellido', 'direccion', 'listar_promociones')
    list_filter = (UsuarioConRolFilter,)

    def listar_promociones(self, obj):
        promociones = obj.promociones.all()  # 'promociones' es el related_name que usamos en PromoPorCliente
        if promociones:
            return format_html(", ".join([str(promo.promo) for promo in promociones]))
        return "No tiene promociones"
    
    listar_promociones.short_description = 'Promociones'

admin.site.register(models.Cliente, ClientesAdmin)

class PromoPorClienteAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente','promo','inicio_promo','fin_promo', 
    'fecha_pago_promo', 'bidones_disponibles', 'entrega_bidones','retorno_bidones',
    'bidones_acumulados','codigo_dispenser','nota')
    list_display = ('id','cliente','promo','fecha_pago_promo', 'inicio_promo','estado')
    list_filter = (UsuarioConRolFilter,)
    
admin.site.register(models.PromoPorCliente, PromoPorClienteAdmin)




