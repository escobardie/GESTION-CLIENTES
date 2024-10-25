from django.urls import path, include
from . import views


urlpatterns = [
    path('listar_visitas/<int:id>', views.ListarVisitasView.as_view(), name='listar_visitas'),
    path('cargar_visita/<int:id>', views.VisitaCreateView.as_view(), name='cargar_visita'),
]
