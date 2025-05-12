from django.urls import path, include
from . import views


urlpatterns = [
    path('crear_suscriptor/', views.CrearSuscriptorView.as_view(), name='crear_suscriptor'),
    
    path('crear_suscripcion/', views.SuscripcionCreateView.as_view(), name='crear_suscripcion'),
    path('crear_suscrip_clte/', views.CrearSuscripcionPorUsuarioView.as_view(), name='crear_suscrip_clte'),
    path('registrar_pago/', views.RegistrarPagoSuscriptorView.as_view(), name='registrar_pago'), 
    path('lista_pagos/', views.ListaPagosView.as_view(), name='lista_pagos'),

    path('pago/<int:pk>/recibo/', views.ReciboPagoImprimibleView.as_view(), name='recibo_pago'),
    path('api/obtener-suscripcion/', views.ObtenerSuscripcionDeUsuarioView.as_view(), name='obtener_suscripcion_usuario'),

    path('pago/recibo/<str:token>/', views.ReciboPagoConTokenView.as_view(), name='recibo_pago_token'),
    path('pagos/recibo/<str:token>/pdf/', views.recibo_pdf_view, name='recibo_pago_pdf'),

]
