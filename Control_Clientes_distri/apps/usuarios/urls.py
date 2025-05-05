from django.urls import path
from . import views

urlpatterns = [
    path('subusuarios/', views.listar_subusuarios, name='listado_subusuarios'),
    path('subusuarios/editar/<int:subusuario_id>/', views.editar_subusuario, name='editar_subusuario'),
    path('subusuarios/eliminar/<int:subusuario_id>/', views.eliminar_subusuario, name='eliminar_subusuario'),
    path('crear_subusuario/', views.crear_subusuario, name='crear_subusuario'), 

    path('login/', views.LoginPersonalizadoView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('acceso-denegado/', views.AccesoDenegadoView.as_view(), name='acceso_denegado'),
]
