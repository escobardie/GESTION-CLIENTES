from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'), # ORIGINAL
    path('listar_clientes/', views.ListarClientesView.as_view(), name='listar_clientes'),
    # path('listar_visitas/<int:id>', views.ListarVisitasView.as_view(), name='listar_visitas'),
    # path('listar_productos/', views.ListarProductosView.as_view(), name='listar_productos'),
    
    # path('listar_pago/', views.ListarPagoClienteView.as_view(), name='listar_pago'),
    # path('listar_pago_cliente/<int:id>', views.ListarPagoClienteView.as_view(), name='listar_pago_cliente'),

    # path('listar_venta/', views.ListarVentaClienteView.as_view(), name='listar_ventas'),
    # path('listar_venta_cliente/<int:id>', views.ListarVentaClienteView.as_view(), name='listar_venta_cliente'),
    
    # path('info_venta/<int:id>', views.DetalleVentaListView.as_view(), name='info_venta'),


    # GESTION VENTAS
    # path('crear_producto/', views.ProductoCreateView.as_view(), name='crear_producto'),
    # path('crear_venta/', views.VentaCreateView.as_view(), name='crear_venta'),

    ## FUNCIONAL 
    # path('crear_venta_producto/', views.VentaProductoCreateView.as_view(), name='crear_venta_producto'),
    # path('crear_venta_producto/<int:id>/', views.VentaProductoCreateView.as_view(), name='crear_venta_producto_cliente'),
    ## FUNCIONAL

    # GESTION PAGOS
    # path('crear_pago/', views.PagoCreateView.as_view(), name='crear_pago'),
    # path('crear_pago_cliente/<int:id>/', views.PagoClienteCreateView.as_view(), name='crear_pago_cliente'),

    path('cargar_cliente/', views.ClienteCreateView.as_view(), name='cargar_cliente'),
    # path('cargar_visita/<int:id>', views.VisitaCreateView.as_view(), name='cargar_visita'),

    #path('promo_por_cliente/<int:id>/<int:promo_id>', views.PromoPorClienteCreateView.as_view(), name='promo_por_cliente'), #ORIGILA
    path('promo_por_cliente/<int:id>', views.PromoPorClienteCreateView.as_view(), name='promo_por_cliente'),
    
    path('menu_cliente/<int:id>', views.MenuClienteDetailView.as_view(), name='menu_cliente'),
    

    
    
    path('servis_visita/<slug:pk>', views.ServisVisitaUpdateView.as_view(), name='servis_visita'),
    
]
