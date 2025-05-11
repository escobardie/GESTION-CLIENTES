from django.urls import path, include
from . import views


urlpatterns = [
    path('crear_suscripcion/', views.SuscripcionCreateView.as_view(), name='crear_suscripcion'),
    path('crear_suscrip_clte/', views.CrearSuscripcionPorUsuarioView.as_view(), name='crear_suscrip_clte'),
    path('registrar_pago/', views.RegistrarPagoSuscriptorView.as_view(), name='registrar_pago'), 
    path('lista_pagos/', views.ListaPagosView.as_view(), name='lista_pagos'),

     path('api/obtener-suscripcion/', views.ObtenerSuscripcionDeUsuarioView.as_view(), name='obtener_suscripcion_usuario'),

    
]
