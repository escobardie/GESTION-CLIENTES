from django.urls import path, include
from . import views


urlpatterns = [
    path('nueva_promo/', views.PromoCreateView.as_view(), name='nueva_promo'),
]
