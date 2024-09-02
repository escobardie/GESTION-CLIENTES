from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'), # ORIGINAL
    path('cargar_cliente/', views.ClienteCreateView.as_view(), name='cargar_cliente'),
    path('cargar_visita/', views.VisitaCreateView.as_view(), name='cargar_visita'),
]
