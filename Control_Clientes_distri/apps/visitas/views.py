from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.usuarios.mixins import ClienteAutorizacionMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.utils.html import mark_safe
from django.urls import reverse
import qrcode
import base64
from io import BytesIO
from itertools import chain


# def usuario_es_admin(user):
#     return  user.groups.filter(name='admin').exists()
def generar_qr_base64(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVisitasClienteView(LoginRequiredMixin, ClienteAutorizacionMixin, ListView):
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
        visitas_combinadas = sorted(
            chain(
                models.Visita.objects.filter(usuario=usuario),
                models.VisitaServis.objects.filter(usuario=usuario)
            ),
            key=lambda x: x.fecha_visita,
            reverse=True
        )
        return visitas_combinadas
        # return models.Visita.objects.filter(
        #     usuario=usuario
        # ).all().order_by('-fecha_visita')


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
class VisitaClienteCreateView(LoginRequiredMixin, ClienteAutorizacionMixin, CreateView): 
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
    
class TicketVisitaImprimibleView(DetailView):
    model = models.Visita
    template_name = 'tickets/visita/ticket_visita.html'
    context_object_name = 'visita'

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        return get_object_or_404(models.Visita, token=token)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visita = self.object

        ticket_url = self.request.build_absolute_uri(self.request.path)
        qr_b64 = generar_qr_base64(ticket_url)

        context['qr_base64'] = mark_safe(f"data:image/png;base64,{qr_b64}")
        context['ticket_url'] = ticket_url

        ticket_url = self.request.build_absolute_uri(
            reverse('ticket_visita', kwargs={'token': visita.token})
        )
        context['ticket_url'] = ticket_url
        context['mensaje'] = (
            f"Hola {visita.cliente}, "
            f"Fuiste visitado el {visita.fecha_visita.strftime('%d/%m/%Y a las %H:%M')}."
            f"Aquí tienes tu ticket Visita: {self.request.build_absolute_uri(self.request.path)}"
        )
        return context
    
class TicketVisitaImprimibleTokenView(DetailView):
    model = models.VisitaServis
    template_name = 'tickets/visita/ticket_visita.html'
    context_object_name = 'visita'

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        return get_object_or_404(models.VisitaServis, token=token)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visita = self.object

        ticket_url = self.request.build_absolute_uri(self.request.path)
        qr_b64 = generar_qr_base64(ticket_url)

        context['qr_base64'] = mark_safe(f"data:image/png;base64,{qr_b64}")
        context['ticket_url'] = ticket_url

        ticket_url = self.request.build_absolute_uri(
            reverse('ticket_visita_token', kwargs={'token': visita.token})
        )
        # pdf_url = self.request.build_absolute_uri(
        #     reverse('recibo_pago_pdf', kwargs={'token': visita.token})
        # )

        context['ticket_url'] = ticket_url
        # context['pdf_url'] = pdf_url


        context['mensaje'] = (
            f"Hola {visita.cliente}, "
            f"Promocion: {visita.nombre_promocion}, "
            f"FFuiste visitado el {visita.fecha_visita.strftime('%d/%m/%Y a las %H:%M')}."
            f"Aquí tienes tu ticket Visita: {self.request.build_absolute_uri(self.request.path)}"
        )


        return context