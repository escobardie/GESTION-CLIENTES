from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


class UsuarioConRolFilter(admin.SimpleListFilter):
    title = 'Usuario (rol=usuario)'  # Texto que aparece en el filtro lateral
    parameter_name = 'usuario'

    def lookups(self, request, model_admin):
        # Lista de usuarios con rol = 'usuario'
        usuarios = Usuario.objects.filter(rol='usuario')
        return [(u.id, u.username) for u in usuarios]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(usuario_padre__id=self.value())
        return queryset



@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y Cliente', {
            'fields': ('rol', 'usuario_padre', 'telefono', 'empresa_nombre')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol y Cliente', {
            'fields': ('rol', 'usuario_padre', 'telefono', 'empresa_nombre')
        }),
    )

    list_display = ('username', 'email', 'rol', 'usuario_padre', 'telefono', 'cantidad_subusuarios', 'is_staff')
    list_filter = (UsuarioConRolFilter,)

    def cantidad_subusuarios(self, obj):
        if obj.es_usuario:
            return obj.empleados.count()
        return '-'
    cantidad_subusuarios.short_description = 'Subusuarios'
