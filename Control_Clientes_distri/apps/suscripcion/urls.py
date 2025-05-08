from django.urls import path, include
from . import views


urlpatterns = [
    path('crear_suscripcion/', views.SuscripcionCreateView.as_view(), name='crear_suscripcion'),
    path('crear_suscrip_clte/', views.CrearSuscripcionPorUsuarioView.as_view(), name='crear_suscrip_clte'),
]
