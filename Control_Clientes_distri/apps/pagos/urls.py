from django.urls import path, include
from . import views


urlpatterns = [
    path('listar_pagos/', views.ListarPagosView.as_view(), name='listar_pagos'),
    path('listar_pago_cliente/<int:id>', views.ListarPagoClienteView.as_view(), name='listar_pago_cliente'),
    path('crear_pago/', views.PagoCreateView.as_view(), name='crear_pago'),
    path('crear_pago_cliente/<int:id>/', views.PagoClienteCreateView.as_view(), name='crear_pago_cliente'),
    path('pago/cliente/recibo/<str:token>/', views.TicketPagosImprimibleTokenView.as_view(), name='pago_cliente_recibo_token'),
]
