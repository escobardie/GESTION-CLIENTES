from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import models, forms
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from datetime import datetime


from django.utils import timezone
from django.contrib import messages

# Create your views here.
# class InicioView(TemplateView): ## ORIGINAL
#     template_name = "Agua/index.html"
#     context_object_name = "inicio_page"

class InicioView(ListView):
    ## TODO SE DEBNE DE AGREGAR EL ORDEN POR FECHA 
    model: models.Cliente
    template_name = "Agua/index.html"
    context_object_name = "lista_clientes"
    paginate_by = 10
    #queryset = models.Cliente.objects.filter(estado=True).order_by('fecha_cobro') ## ORIGINAL
    #queryset = models.Cliente.objects.filter(estado=True).order_by('nombre')
    def get_queryset(self):
        # Filtrar los clientes cuyo estado es True y ordenar por fecha de creación
        queryset = models.Cliente.objects.filter(estado=True).order_by('fecha_cobro')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener la fecha actual
        fecha_actual = timezone.now().date()
        # Filtrar clientes con fecha de cobro vencida
        clientes_con_fecha_vencida = self.get_queryset().filter(fecha_cobro__lt=fecha_actual)
        # Pasar esta información al contexto
        context['clientes_con_fecha_vencida'] = clientes_con_fecha_vencida
        return context

class ListarClientesView(ListView):
    model = models.Cliente
    template_name = "Agua/listar_clientes.html"
    context_object_name = 'lista_clientes'
    paginate_by = 5
    queryset = models.Cliente.objects.filter(estado=True)

class ListarVisitasView(ListView):
    model = models.Visita
    template_name = "Agua/listar_vistas.html"
    context_object_name = 'lista_vistas'
    paginate_by = 5
    # queryset = models.Visita.objects.filter(estado=True)
    def get_cliente_data(self):
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente
    
    def get_queryset(self):
        cliente = self.get_cliente_data()
        return models.Visita.objects.filter(cliente=cliente).order_by('-fecha_visita')



class MenuClienteDetailView(DetailView):
    model = models.Cliente
    template_name = "Agua/menu_cliente.html"
    context_object_name = 'cliente'

    def get_object(self):
        # Obtén el parámetro 'id' desde la URL
        cliente_id = self.kwargs.get('id')
        # Busca el cliente por su 'id'. Si no se encuentra, arroja un error 404.
        return get_object_or_404(models.Cliente, id=cliente_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()  # Obtén el cliente

        # Filtrar promociones relacionadas con el cliente
        context['tipo_promocion'] = models.Promo.objects.filter(cliente=cliente)
        
        return context

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
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VisitaCreateView(CreateView):
    template_name = 'Agua/forms/visita.html'
    form_class = forms.AddVisitaForm
    
    def get_cliente_data(self):
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar el nombre del cliente al contexto
        # cliente_id = self.kwargs['id']
        # cliente = get_object_or_404(models.Cliente, id=cliente_id)
        cliente = self.get_cliente_data()
        context['nombre_cliente'] = cliente  # Obtener el nombre del cliente
        return context

    def get_initial(self):
        # Obtener el cliente específico
        # cliente_id = self.kwargs['id']
        # cliente = get_object_or_404(models.Cliente, id=cliente_id)
        cliente = self.get_cliente_data()
        # Retornar los valores iniciales del formulario
        return {'cliente': cliente}

    def form_valid(self, form):
        # # Obtener el cliente específico desde los kwargs
        # cliente = self.get_cliente_data()
        # # Asignar el cliente al formulario antes de guardarlo
        # visita = form.save(commit=False)
        # visita.cliente = cliente
        form.save()  # Guardar el formulario
        return super().form_valid(form)

    def get_success_url(self):
        # Obtiene el ID del cliente desde los kwargs
        cliente_id = self.kwargs.get('id')
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})
    
## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PromoPorClienteCreateView(CreateView):
    template_name = 'Agua/forms/promo_x_cliente.html'
    form_class = forms.AddPromoPorClienteForm

    # def get_cliente_data(self):
    #     cliente_id = self.kwargs['id']
    #     cliente = get_object_or_404(models.Cliente, id=cliente_id)
    #     return cliente

    def get_initial(self):
        # Obtener el cliente específico
        cliente_id = self.kwargs['id']
        promo_id = self.kwargs['promo_id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        promo = get_object_or_404(models.Promo, id=promo_id)
        fecha_actual = datetime.now().date().isoformat()  # 'YYYY-MM-DD'  # Obtiene solo la fecha actual
        # Acceder al campo `cant_bidones` de la instancia de `promo`
        bidones_disponibles = promo.cant_bidones
        # Retornar los valores iniciales del formulario
        # return {'cliente': cliente, 'promo':promo} # ORIGINAL
        return {
            'cliente': cliente, 
            'promo': promo, 
            'inicio_promo': fecha_actual, 
            'bidones_disponibles': bidones_disponibles
        }

    def form_valid(self, form):
        form.save()  # Guardar el formulario
        return super().form_valid(form)

    def get_success_url(self):
        # Obtiene el ID del cliente desde los kwargs
        cliente_id = self.kwargs.get('id')
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})