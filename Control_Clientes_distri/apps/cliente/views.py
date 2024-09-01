from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.
class InicioView(TemplateView):
    template_name = "Agua/index.html"
    context_object_name = "inicio_page"