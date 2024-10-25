from django.urls import path, include
from . import views


urlpatterns = [
    path('listar_pago/', views.ListarPagoClienteView.as_view(), name='listar_pago'),
    path('listar_pago_cliente/<int:id>', views.ListarPagoClienteView.as_view(), name='listar_pago_cliente'),
    path('crear_pago/', views.PagoCreateView.as_view(), name='crear_pago'),
    path('crear_pago_cliente/<int:id>/', views.PagoClienteCreateView.as_view(), name='crear_pago_cliente'),

]
