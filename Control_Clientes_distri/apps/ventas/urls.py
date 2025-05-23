from django.urls import path, include
from . import views


urlpatterns = [
    # path('crear-venta/', views.CrearVentaView.as_view(), name='crear_venta'),
    
    path('listar_venta/', views.ListarVentasView.as_view(), name='listar_ventas'),
    path('listar_venta_cliente/<int:id>', views.ListarVentaClienteView.as_view(), name='listar_venta_cliente'),
    
    path('info_venta/<int:id>', views.DetalleVentaListView.as_view(), name='info_venta'),

    path('crear_venta_producto/', views.CrearVentaView.as_view(), name='crear_venta_producto'),
    path('crear_venta_producto/<int:id>/', views.CrearVentaView.as_view(), name='crear_venta_producto_cliente'),
    
]
