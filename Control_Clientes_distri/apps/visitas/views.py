from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin


# def usuario_es_admin(user):
#     return  user.groups.filter(name='admin').exists()


# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVisitasClienteView(LoginRequiredMixin, ListView):
    model = models.Visita
    template_name = "base/listar_vistas_cliente.html"
    context_object_name = 'lista_vista_cliente'
    paginate_by = 5
    
    def get_cliente_data(self):
        # ['id'] = Este acceso es más directo y espera que la clave 'id' exista en el diccionario kwargs
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente
    
    def get_queryset(self):
        cliente = self.get_cliente_data()
        return models.Visita.objects.filter(cliente=cliente).order_by('-fecha_visita')

# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVisitasView(LoginRequiredMixin, ListView):
    model = models.Visita
    template_name = "base/listar_vistas.html"
    context_object_name = 'lista_vistas'
    paginate_by = 5

    
    # def get_queryset(self):
    #     return models.Visita.objects.all().order_by('-fecha_visita')
    
    def get_queryset(self):
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.cliente
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        return models.Visita.objects.filter(
            usuario=usuario
        ).all().order_by('-fecha_visita')


## se agrega capa de seguridad para la carga de datos
# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VisitaCreateView(LoginRequiredMixin, CreateView):
    model = models.Visita
    template_name = 'base/forms/crear_visita.html'
    form_class = forms.AddVisitaForm
    success_url = reverse_lazy('listar_visitas')
    
    def form_valid(self, form):
        # Si es subusuario, usar su cliente asociado
        usuario_asociado = (
            self.request.user.cliente
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        visita = form.save(commit=False)
        visita.usuario = usuario_asociado
        visita.cliente = None ## visita creada para no clientes
        visita.save()  # Guardar el formulario
        return super().form_valid(form)

# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VisitaClienteCreateView(LoginRequiredMixin, CreateView): 
    template_name = 'base/forms/crear_visita_cliente.html'
    form_class = forms.AddVisitaForm
    
    def get_cliente_data(self):
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente

    def get_initial(self):
        # Obtener el cliente específico
        cliente = self.get_cliente_data()
        # Retornar los valores iniciales del formulario
        return {'cliente': cliente}

    def form_valid(self, form): ## original
        # Si es subusuario, usar su cliente asociado
        usuario_asociado = (
            self.request.user.cliente
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        # form.save()  # Guardar el formulario
        form.instance.usuario = usuario_asociado
        return super().form_valid(form)

    def get_success_url(self):
        # Obtiene el ID del cliente desde los kwargs
        cliente_id = self.kwargs.get('id') ## USAMOS ESTE PORQUE EL USAMOS EL FORMULARIO PREDETERMIANDO "{{ form.as_p }}"
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})