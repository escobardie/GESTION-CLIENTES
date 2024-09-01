from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio') # ORIGINAL
    #path('signup/', views.SignUpView.as_view(), name='signup'),
]
