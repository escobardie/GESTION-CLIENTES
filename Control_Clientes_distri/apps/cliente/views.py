from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from . import models, forms
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from datetime import datetime
from apps.visitas.models import Visita, VisitaServis
from apps.pagos.models import Pagos
from apps.ventas.models import Venta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from apps.usuarios.mixins import ClienteAutorizacionMixin
from itertools import chain


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "base/listar_clientes.html"


class ListarVencimientoView(LoginRequiredMixin,ListView):
    model = models.PromoPorCliente
    template_name = "base/listar_vencimiento_clte.html"
    context_object_name = "listar_promos"
    paginate_by = 10


    def get_queryset(self):
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )

        return models.PromoPorCliente.objects.filter(
            estado=True,
            usuario=usuario
        ).order_by('fecha_pago_promo')
    
    def get_promos_que_vencen_hoy(self):
        fecha_actual = timezone.now().date()
        return self.get_queryset().filter(fecha_pago_promo=fecha_actual)
    
    def get_promos_con_fecha_vencida(self):
        fecha_actual = timezone.now().date()
        return self.get_queryset().filter(fecha_pago_promo__lt=fecha_actual)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promos_que_vencen_hoy'] = self.get_promos_que_vencen_hoy()
        context['promos_con_fecha_vencida'] = self.get_promos_con_fecha_vencida()
        return context
    ## TODO: AGREGAR OPCION DE ENVIAR MSJ DE WAP AL CLIENTE. CON LA LEYERNDA DE "CUOTA PRONTO A VENCER"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     queryset = self.get_queryset()
    #     fecha_actual = timezone.now().date()
    #     promo_con_fecha_vencida = queryset.filter(fecha_pago_promo__lt=fecha_actual)
    #     context['promos_con_fecha_vencida'] = promo_con_fecha_vencida
    #     return context


class ListarClientesView(LoginRequiredMixin, ListView):
    model = models.Cliente
    template_name = "base/listar_clientes.html"
    context_object_name = 'lista_clientes'
    paginate_by = 5

    def get_queryset(self):
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )

        return models.Cliente.objects.filter(
            estado=True,
            usuario=usuario
        ).order_by('apellido')


class MenuClienteDetailView(LoginRequiredMixin,ClienteAutorizacionMixin, DetailView):
    model = models.Cliente
    template_name = "base/menu_cliente2.html"
    context_object_name = 'cliente'

    # def dispatch(self, request, *args, **kwargs):
    #     self.cliente_obj = get_object_or_404(models.Cliente, id=self.kwargs['id'])
    #     usuario_actual = (
    #         request.user.usuario_padre
    #         if request.user.rol == 'subusuario'
    #         else request.user
    #     )
    #     if self.cliente_obj.usuario != usuario_actual:
    #         return redirect('acceso_denegado')
    #     return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.cliente_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        fecha_actual = timezone.now().date()
        estado_promo_vencida = False
        estado_promo_por_vencer = False

        ## metodo para obtener mas datos
        promocion_del_cliente = models.PromoPorCliente.objects \
            .filter(cliente=cliente, estado=True) \
            .values('id', 'promo__nombre_promo', 'promo__valor_promo', 'fecha_pago_promo', 'bidones_disponibles', 'bidones_acumulados') \
            .first()

        ## obtenemos de este modo el ultimo pago de la promocion    
        ultimo_pago_promo = Pagos.objects \
            .filter(cliente=cliente,promo__isnull=False) \
            .values('id','fecha_pago') \
            .first()
        
        ## HACEMOS UN FILTRO GENERAL
        visitas = Visita.objects.filter(cliente=cliente)
        visitas_servis = VisitaServis.objects.filter(cliente=cliente)
        # Agregar el tipo de modelo a cada instancia
        for v in visitas:
            v.tipo = 'visita'
        for vs in visitas_servis:
            vs.tipo = 'visita_servis'

        ## HACEMOS UN FILTRO MAS ESPECIFICO
        ultima_visita = visitas.order_by('-fecha_visita').first()
        ultima_visitaServis = visitas_servis.order_by('-fecha_visita').first()

        # ultima_visita = Visita.objects.filter(cliente=cliente).order_by('-fecha_visita').first()
        # ultima_visitaServis = VisitaServis.objects.filter(cliente=cliente).order_by('-fecha_visita').first()

        # Obtener fechas si existen
        fecha1 = ultima_visita.fecha_visita if ultima_visita else None
        fecha2 = ultima_visitaServis.fecha_visita if ultima_visitaServis else None

        # Comparar y obtener la más reciente
        if fecha1 and fecha2:
            fecha_visita_clte = max(fecha1, fecha2).date()
        elif fecha1:
            fecha_visita_clte = fecha1.date()
        elif fecha2:
            fecha_visita_clte = fecha2.date()
        else:
            fecha_visita_clte = "Sin visitas"

        ultima_pago = models.PromoPorCliente.objects.filter(cliente=cliente, estado=True).order_by('fecha_pago_promo').first()
        if ultima_pago and ultima_pago.fecha_pago_promo < fecha_actual:
            estado_promo_vencida = True
        if ultima_pago and ultima_pago.fecha_pago_promo == fecha_actual:
            estado_promo_por_vencer = True

        fecha_pago_clte = ultima_pago.fecha_pago_promo if ultima_pago else "Sin Pagos Realizados"
        
        visitas_combinadas = sorted(
            chain(visitas, visitas_servis),
            key=lambda x: x.fecha_visita,
            reverse=True
        )[:10]

        context.update({
            'pagos_cliente': Pagos.objects.filter(cliente=cliente).order_by('-fecha_pago')[:10],
            'ventas_cliente': Venta.objects.filter(cliente=cliente).order_by('-fecha_venta')[:10],
            'visitas_combinadas': visitas_combinadas,
            'fecha_pago': fecha_pago_clte,
            'fecha_visita': fecha_visita_clte,
            'promocion': promocion_del_cliente,
            'promo_vencida': estado_promo_vencida,            
            'promo_por_vencer': estado_promo_por_vencer,
            
            'ultimo_pago_promo': ultimo_pago_promo,
        })
        return context
    
# @method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = models.Cliente
    template_name = 'base/forms/crear_cliente.html'
    form_class = forms.AddClienteForm

    def get_success_url(self):
        return reverse('menu_cliente', kwargs={'id': self.object.id})

    def form_valid(self, form):
        # Si es subusuario, usar su cliente asociado
        usuario_asociado = (
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        form.instance.usuario = usuario_asociado
        return super().form_valid(form)

# @method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class PromoPorClienteCreateView(LoginRequiredMixin, ClienteAutorizacionMixin, CreateView):
    template_name = 'base/forms/promo_x_cliente.html'
    form_class = forms.AddPromoPorClienteForm

    def get_initial(self):
        fecha_actual = timezone.now().date()
        cliente_id = self.kwargs['id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        un_año_default = ( fecha_actual + relativedelta(years=1)).isoformat()
        un_mes_default = ( fecha_actual + relativedelta(months=1)).isoformat()
        return {'cliente': cliente, 'fin_promo': un_año_default, 'fecha_pago_promo': un_mes_default}
    
    def get_form_kwargs(self):
        ## usamos esto para enviar el usuario al form y asi filtrar sus propias promociones.
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Aquí pasamos el usuario al formulario
        return kwargs

    def form_valid(self, form):
        # Si es subusuario, usar su cliente asociado
        usuario_asociado = (
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        promo_id = form.cleaned_data['promo'].id
        promo_instance = get_object_or_404(models.Promo, id=promo_id)
        fecha_actual = datetime.now().date().isoformat()
        dibones_disponibles_promo = promo_instance.cant_bidones
        promocliente = form.save(commit=False)
        promocliente.inicio_promo = fecha_actual
        promocliente.bidones_disponibles = dibones_disponibles_promo
        form.instance.usuario = usuario_asociado
        promocliente.save()
        return super().form_valid(form)

    def get_success_url(self):
        cliente_id = self.kwargs.get('id')
        return reverse('crear_pago_cliente', kwargs={'id': cliente_id})
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_id'] =  self.kwargs.get('id')
        return context

# @method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
class ServisVisitaUpdateView(LoginRequiredMixin, UpdateView):
    model = models.PromoPorCliente
    template_name = 'base/forms/servis_visita_cliente.html'
    form_class = forms.ServisVisitaClienteForm
    slug_field = 'slug'
    slug_url_kwarg = 'pk'

    def dispatch(self, request, *args, **kwargs):
        self.cliente_obj = get_object_or_404(models.Cliente, id=self.kwargs['pk'])
        usuario_actual = (
            request.user.usuario_padre
            if request.user.rol == 'subusuario'
            else request.user
        )
        if self.cliente_obj.usuario != usuario_actual:
            return redirect('acceso_denegado')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        cliente_id = self.kwargs.get('pk')
        id_promo = self.request.GET.get('id_promo')
        return get_object_or_404(models.PromoPorCliente, cliente_id=cliente_id, id=id_promo)

    def get_cliente_data(self):
        cliente_id = self.kwargs['pk']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente

    def form_valid(self, form):
        # Si es subusuario, usar su cliente asociado
        usuario_asociado = (
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        cliente = self.get_cliente_data()
        promo_id = self.request.GET.get('id_promo')
        bidones_disponibles = int(self.request.POST.get('bidones_disponibles'))
        entrega_bidones = int(self.request.POST.get('entrega_bidones'))
        retorno_bidones = int(self.request.POST.get('retorno_bidones'))
        bidones_acumulados = int(self.request.POST.get('bidones_acumulados'))
        observacion_visita = self.request.POST.get('observacion_visita')

        PromoPorCliente = form.save(commit=False)
        PromoPorCliente.entrega_bidones = 0
        PromoPorCliente.retorno_bidones = 0
        PromoPorCliente.save()

        promo = get_object_or_404(models.PromoPorCliente, id=promo_id)
        visitaservis = VisitaServis.objects.create(
            usuario=usuario_asociado,
            cliente=cliente,
            nombre_promocion=promo.promo.nombre_promo,
            b_disponible=bidones_disponibles,
            b_entregado=entrega_bidones,
            b_retirado=retorno_bidones,
            b_en_poder_clte=bidones_acumulados,
            nota=observacion_visita
        )
        return super().form_valid(form)

    def get_success_url(self):
        cliente_id = self.kwargs.get('pk')
        return reverse('menu_cliente', kwargs={'id': cliente_id})





# @method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
# class ListarClientesView(ListView): ## original
#     model = models.Cliente
#     template_name = "base/listar_clientes.html"
#     context_object_name = 'lista_clientes'
#     paginate_by = 5
#     queryset = models.Cliente.objects.filter(estado=True).order_by('apellido')



# @method_decorator(user_passes_test(usuario_es_admin, login_url='index'), name='dispatch')
# class MenuClienteDetailView(LoginRequiredMixin, DetailView): ## ORIGINAL
#     model = models.Cliente
#     template_name = "base/menu_cliente.html"
#     context_object_name = 'cliente'

#     def get_object(self):
#         cliente_id = self.kwargs['id']
#         cliente = get_object_or_404(models.Cliente, id=cliente_id)
#         # Obtener el usuario dueño
#         usuario_actual = (
#             self.request.user.usuario_padre
#             if self.request.user.rol == 'subusuario'
#             else self.request.user
#         )

#         if cliente.usuario != usuario_actual:
#             return redirect('acceso_denegado')
        
#         return cliente

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cliente = self.get_object()
#         fecha_actual = timezone.now().date()
#         estado_promo_vencida = False
#         if cliente:
#             promociones_del_cliente = models.PromoPorCliente.objects.filter(
#                 cliente=cliente,
#                 estado=True
#             ).values('id', 'promo__nombre_promo', 'promo__valor_promo',
#                      'fecha_pago_promo', 'bidones_disponibles', 'bidones_acumulados')
#             # fecha_visita_clte = Visita.objects.filter(
#             #     cliente=cliente
#             # ).values('fecha_visita')
#             ultima_visita = Visita.objects.filter(cliente=cliente).order_by('-fecha_visita').first()
#             if ultima_visita:
#                 fecha_visita_clte = ultima_visita.fecha_visita.date()
#             else:
#                 fecha_visita_clte = "Sin visitas"

#             # ultima_pago = Pagos.objects.filter(cliente=cliente, venta=None).order_by('-fecha_pago').first() # ORIOGINAL
#             ultima_pago = models.PromoPorCliente.objects.filter(cliente=cliente, estado=True).order_by('fecha_pago_promo').first()
#             if ultima_pago:
#                 fecha_pago_clte = ultima_pago.fecha_pago_promo
#                 if fecha_pago_clte < fecha_actual:
#                     estado_promo_vencida = True
#             else:
#                 fecha_pago_clte = "Sin Pagos Realizados"
            
#             visitas_cliente = Visita.objects.filter(cliente=cliente).order_by('-fecha_visita')[:10]
            
#             ventas_cliente = Venta.objects.filter(cliente=cliente).order_by('-fecha_venta')[:10]
            
#             pagos_cliente = Pagos.objects.filter(cliente=cliente).order_by('-fecha_pago')[:10]

#             context['pagos_cliente'] = pagos_cliente
#             context['ventas_cliente'] = ventas_cliente
#             context['visitas_cliente'] = visitas_cliente
#             context['fecha_pago'] = fecha_pago_clte
#             context['fecha_visita'] = fecha_visita_clte
#             context['promociones'] = promociones_del_cliente
#             context['promo_vencida'] = estado_promo_vencida
#         return context