from django.urls import path, include
from . import views


urlpatterns = [
    path('cargar_visita/', views.VisitaCreateView.as_view(), name='cargar_visita'),
    path('cargar_visita_cliente/<int:id>', views.VisitaClienteCreateView.as_view(), name='cargar_visita_cliente'),
    path('listar_visitas_cliente/<int:id>', views.ListarVisitasClienteView.as_view(), name='listar_visitas_cliente'),
    path('listar_visitas/', views.ListarVisitasView.as_view(), name='listar_visitas'),
    
    path('visitas/ticket/<str:token>/', views.TicketVisitaImprimibleView.as_view(), name='ticket_visita'),
    path('visitas/ticket/token/<str:token>/', views.TicketVisitaImprimibleTokenView.as_view(), name='ticket_visita_token'),

]
