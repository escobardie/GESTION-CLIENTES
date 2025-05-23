from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardEstadisticasView.as_view(), name='dashboard_estadisticas'),
    path('api/ventas/', views.VentasAPI.as_view(), name='api_ventas'), 
    path('api/pagos_semana/', views.PagosSemanaAPI.as_view(), name='api_pagos_semana'),
    path('api/pagos/', views.PagosAPI.as_view(), name='api_pagos'),
    path('api/ultimos_meses/', views.Pagos6MesesAPI.as_view(), name='api_pagos_ultimos_6_meses'),
    path('api/pagos_recientes/', views.PagosRecientesAPI.as_view(), name='api_pagos_recientes'),
    path('api/productos/', views.ProductosMasVendidosAPI.as_view(), name='api_productos'),
    path('api/count_clientes/', views.CountClientesAPI.as_view(), name='api_count_clientes'),

]
