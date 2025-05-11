# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y Cliente', {
            'fields': ('rol', 'cliente', 'telefono', 'empresa_nombre')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol y Cliente', {
            'fields': ('rol', 'cliente', 'telefono', 'empresa_nombre')
        }),
    )

    list_display = ('username', 'email', 'rol', 'cliente', 'telefono', 'cantidad_subusuarios', 'is_staff')
    list_filter = ('rol',)

    def cantidad_subusuarios(self, obj):
        if obj.es_cliente():
            return obj.empleados.count()
        return '-'
    cantidad_subusuarios.short_description = 'Subusuarios'
