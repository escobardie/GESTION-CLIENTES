from django.urls import path
from . import views

urlpatterns = [
    # path('dashboard/', views.dashboard_estadisticas, name='dashboard_estadisticas'),
    # path('api/ventas/', views.api_ventas_data, name='api_ventas'),
    # path('api/pagos/', views.api_pagos_data, name='api_pagos'),
    # path('api/pagos_recientes/', views.api_pagos_recientes, name='api_pagos_recientes'),
    # path('api/productos/', views.api_productos_mas_vendidos, name='api_productos'),

    path('dashboard/', views.DashboardEstadisticasView.as_view(), name='dashboard_estadisticas'),
    path('api/ventas/', views.VentasAPI.as_view(), name='api_ventas'),
    path('api/pagos/', views.PagosAPI.as_view(), name='api_pagos'),
    path('api/pagos_recientes/', views.PagosRecientesAPI.as_view(), name='api_pagos_recientes'),
    path('api/productos/', views.ProductosMasVendidosAPI.as_view(), name='api_productos'),

]
