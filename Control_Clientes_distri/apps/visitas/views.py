from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse
from . import models, forms


def usuario_es_admin(user):
    return  user.groups.filter(name='admin').exists()


@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVisitasView(ListView):
    model = models.Visita
    template_name = "base/listar_vistas.html"
    context_object_name = 'lista_vistas'
    paginate_by = 5
    
    def get_cliente_data(self):
        # ['id'] = Este acceso es más directo y espera que la clave 'id' exista en el diccionario kwargs
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente
    
    def get_queryset(self):
        cliente = self.get_cliente_data()
        return models.Visita.objects.filter(cliente=cliente).order_by('-fecha_visita')

## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VisitaCreateView(CreateView):
    template_name = 'base/forms/visita_cliente.html'
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
        form.save()  # Guardar el formulario
        return super().form_valid(form)

    def get_success_url(self):
        # Obtiene el ID del cliente desde los kwargs
        cliente_id = self.kwargs.get('id') ## USAMOS ESTE PORQUE EL USAMOS EL FORMULARIO PREDETERMIANDO "{{ form.as_p }}"
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})