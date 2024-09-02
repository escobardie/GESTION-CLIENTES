from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
class InicioView(TemplateView):
    template_name = "Agua/index.html"
    context_object_name = "inicio_page"





################# CRUD ####################

def usuario_es_admin(user):
    return  user.groups.filter(name='admin').exists()

## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ClienteCreateView(CreateView):
    model = models.Cliente
    template_name = 'Agua/forms/crear_cliente.html'
    form_class = forms.AddClienteForm
    success_url = reverse_lazy('inicio')
    
    def form_invalid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VisitaCreateView(CreateView):
    model = models.Visita
    template_name = 'Agua/forms/visita.html'
    form_class = forms.AddVisitaForm
    success_url = reverse_lazy('inicio')

    def form_invalid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
        
    