from django.contrib import admin
from .models import Suscripcion, SuscripcionPorUsuario, PagoSuscriptor

@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_suscripcion',
        'valor_suscripcion',
        'fecha_alta',
        'fecha_vencimiento',
        'estado',
    )
    list_filter = ('estado', 'fecha_alta', 'fecha_vencimiento')
    search_fields = ('nombre_suscripcion',)
    ordering = ('-fecha_alta',)
    readonly_fields = ('fecha_alta',)

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(SuscripcionPorUsuario)
class SuscripcionPorUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'suscripcion',
        'fecha_asignacion',
        'fecha_cobro_suscrip',
        'fecha_fin_suscrip',
        'estado',
    )
    list_filter = ('estado', 'fecha_asignacion', 'fecha_cobro_suscrip', 'fecha_fin_suscrip')
    search_fields = ('usuario__username', 'suscripcion__nombre_suscripcion')
    ordering = ('-fecha_asignacion',)
    readonly_fields = ('fecha_asignacion',)

    fieldsets = (
        (None, {
            'fields': (
                'usuario',
                'suscripcion',
                'fecha_cobro_suscrip',
                'fecha_fin_suscrip',
                'estado',
                'nota',
                'fecha_asignacion',
            )
        }),
    )


@admin.register(PagoSuscriptor)
class PagoSuscriptorAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'suscripcion',
        'monto',
        'metodo_pago',
        'fecha_pago',
    )
    list_filter = ('metodo_pago', 'fecha_pago')
    search_fields = ('usuario__username', 'suscripcion__nombre_suscripcion')
    ordering = ('-fecha_pago',)
    readonly_fields = ('fecha_pago',)

    fieldsets = (
        (None, {
            'fields': (
                'usuario',
                'suscripcion',
                'monto',
                'metodo_pago',
                'descripcion',
                'fecha_pago',
            )
        }),
    )
