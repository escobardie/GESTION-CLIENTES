from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'), # ORIGINAL
    path('cargar_cliente/', views.ClienteCreateView.as_view(), name='cargar_cliente'),
    path('cargar_visita/<int:id>', views.VisitaCreateView.as_view(), name='cargar_visita'),

    path('promo_por_cliente/<int:id>/<int:promo_id>', views.PromoPorClienteCreateView.as_view(), name='promo_por_cliente'),

    path('menu_cliente/<int:id>', views.MenuClienteDetailView.as_view(), name='menu_cliente'),
    
]
