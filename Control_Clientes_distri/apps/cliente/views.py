from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from . import models, forms
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from datetime import datetime
from apps.visitas.models import Visita
from apps.pagos.models import Pagos
from apps.ventas.models import Venta
from django.utils import timezone


class IndexView(TemplateView):
    template_name = "base/index.html"
    context_object_name = 'index'

def usuario_es_admin(user):
    return user.groups.filter(name='admin').exists()

class ListarVencimientoView(ListView):
    model = models.PromoPorCliente
    template_name = "base/listar_vencimiento_clte.html"
    context_object_name = "listar_promos"
    paginate_by = 10

    def get_queryset(self):
        return models.PromoPorCliente.objects.filter(estado=True).order_by('fecha_pago_promo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        fecha_actual = timezone.now().date()
        promo_con_fecha_vencida = queryset.filter(fecha_pago_promo__lt=fecha_actual)
        context['promos_con_fecha_vencida'] = promo_con_fecha_vencida
        return context

@method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class ListarClientesView(ListView):
    model = models.Cliente
    template_name = "base/listar_clientes.html"
    context_object_name = 'lista_clientes'
    paginate_by = 5
    queryset = models.Cliente.objects.filter(estado=True).order_by('apellido')

@method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class MenuClienteDetailView(DetailView):
    model = models.Cliente
    template_name = "base/menu_cliente.html"
    context_object_name = 'cliente'

    def get_object(self):
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        if cliente:
            promociones_del_cliente = models.PromoPorCliente.objects.filter(
                cliente=cliente,
                estado=True
            ).values('id', 'promo__nombre_promo', 'promo__valor_promo',
                     'fecha_pago_promo', 'bidones_disponibles', 'bidones_acumulados')
            # fecha_visita_clte = Visita.objects.filter(
            #     cliente=cliente
            # ).values('fecha_visita')
            ultima_visita = Visita.objects.filter(cliente=cliente).order_by('-fecha_visita').first()
            if ultima_visita:
                fecha_visita_clte = ultima_visita.fecha_visita.date()
            else:
                fecha_visita_clte = "Sin visitas"

            ultima_pago = Pagos.objects.filter(cliente=cliente, venta=None).order_by('-fecha_pago').first()
            if ultima_pago:
                fecha_pago_clte = ultima_pago.fecha_pago.date()
            else:
                fecha_pago_clte = "Sin Pagos Realizados"
            
            visitas_cliente = Visita.objects.filter(cliente=cliente).order_by('-fecha_visita')[:10]
            
            ventas_cliente = Venta.objects.filter(cliente=cliente).order_by('-fecha_venta')[:10]
            
            pagos_cliente = Pagos.objects.filter(cliente=cliente).order_by('-fecha_pago')[:10]

            context['pagos_cliente'] = pagos_cliente
            context['ventas_cliente'] = ventas_cliente
            context['visitas_cliente'] = visitas_cliente
            context['fecha_pago'] = fecha_pago_clte
            context['fecha_visita'] = fecha_visita_clte
            context['promociones'] = promociones_del_cliente
        return context

@method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class ClienteCreateView(CreateView):
    model = models.Cliente
    template_name = 'base/forms/crear_cliente.html'
    form_class = forms.AddClienteForm

    def get_success_url(self):
        return reverse('menu_cliente', kwargs={'id': self.object.id})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

@method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class PromoPorClienteCreateView(CreateView):
    template_name = 'Agua/forms/promo_x_cliente.html'
    form_class = forms.AddPromoPorClienteForm

    def get_initial(self):
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return {'cliente': cliente}

    def form_valid(self, form):
        promo_id = form.cleaned_data['promo'].id
        promo_instance = get_object_or_404(models.Promo, id=promo_id)
        fecha_actual = datetime.now().date().isoformat()
        dibones_disponibles_promo = promo_instance.cant_bidones
        promocliente = form.save(commit=False)
        promocliente.inicio_promo = fecha_actual
        promocliente.bidones_disponibles = dibones_disponibles_promo
        promocliente.save()
        return super().form_valid(form)

    def get_success_url(self):
        cliente_id = self.kwargs.get('id')
        return reverse('menu_cliente', kwargs={'id': cliente_id})

@method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class ServisVisitaUpdateView(UpdateView):
    model = models.PromoPorCliente
    template_name = 'base/forms/servis_visita_cliente.html'
    form_class = forms.ServisVisitaClienteForm
    slug_field = 'slug'
    slug_url_kwarg = 'pk'

    def get_object(self):
        cliente_id = self.kwargs.get('pk')
        id_promo = self.request.GET.get('id_promo')
        return get_object_or_404(models.PromoPorCliente, cliente_id=cliente_id, id=id_promo)

    def get_cliente_data(self):
        cliente_id = self.kwargs['pk']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente

    def form_valid(self, form):
        cliente = self.get_cliente_data()
        promo_id = self.request.GET.get('id_promo')
        bidones_disponibles = self.request.POST.get('bidones_disponibles')
        entrega_bidones = int(self.request.POST.get('entrega_bidones'))
        retorno_bidones = int(self.request.POST.get('retorno_bidones'))
        bidones_acumulados = self.request.POST.get('bidones_acumulados')
        PromoPorCliente = form.save(commit=False)
        PromoPorCliente.entrega_bidones = 0
        PromoPorCliente.retorno_bidones = 0
        PromoPorCliente.save()
        promo = get_object_or_404(models.PromoPorCliente, id=promo_id)
        visita = Visita.objects.create(
            cliente=cliente,
            # nota="<ul>"+
            #      f"<li>PROMOCION:  {promo.promo.nombre_promo}</li>"+
            #      f"<li>BIDONES DISPONIBLES:  {bidones_disponibles}</li>"+
            #      f"<li>BIDONES ENTREGADOS AL CLIENTE: {entrega_bidones} </li>"+
            #      f"<li>BIDONES RETIRADOS DEL DOMICILIO:{retorno_bidones}</li>"+
            #      f"<li>BIDONES EN PODER DEL CLIENTE: {bidones_acumulados}</li>"+
            #      "</ul>"
            nota =  f"<p><strong>Promoción:</strong> {promo.promo.nombre_promo}</p>"+
                    f"<p><strong>Bidones Disponibles:</strong> {bidones_disponibles}</p>"+
                    f"<p><strong>Bidones Entregados al cliente:</strong> {entrega_bidones}</p>"+
                    f"<p><strong>Bidones Retirados del domicilio:</strong> {retorno_bidones}</p>"+
                    f"<p><strong>Bidones en poder del cliente:</strong> {bidones_acumulados}</p>"
        )
        return super().form_valid(form)

    def get_success_url(self):
        cliente_id = self.kwargs.get('pk')
        return reverse('menu_cliente', kwargs={'id': cliente_id})
