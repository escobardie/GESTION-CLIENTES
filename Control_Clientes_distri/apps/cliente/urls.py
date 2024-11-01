from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('listar_vto_clte/', views.ListarVencimientoView.as_view(), name='listar_vto_clte'),
    path('listar_clientes/', views.ListarClientesView.as_view(), name='listar_clientes'),
    
    path('cargar_cliente/', views.ClienteCreateView.as_view(), name='cargar_cliente'),
    # path('cargar_visita/<int:id>', views.VisitaCreateView.as_view(), name='cargar_visita'),

    #path('promo_por_cliente/<int:id>/<int:promo_id>', views.PromoPorClienteCreateView.as_view(), name='promo_por_cliente'), #ORIGILA
    path('promo_por_cliente/<int:id>', views.PromoPorClienteCreateView.as_view(), name='promo_por_cliente'),
    
    path('menu_cliente/<int:id>', views.MenuClienteDetailView.as_view(), name='menu_cliente'),
    

    
    
    path('servis_visita/<slug:pk>', views.ServisVisitaUpdateView.as_view(), name='servis_visita'),
    
]
