from django.urls import path, include
from . import views


urlpatterns = [
    path('listar_productos/', views.ListarProductosView.as_view(), name='listar_productos'),
    path('crear_producto/', views.ProductoCreateView.as_view(), name='crear_producto'),
    
]
