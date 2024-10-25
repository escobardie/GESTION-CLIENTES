from django.contrib import admin
from . import models 

class VisitaAdmin(admin.ModelAdmin):
    readonly_fields = ('cliente','fecha_visita','nota')
    list_display = ('fecha_visita', 'cliente')

admin.site.register(models.Visita, VisitaAdmin)
