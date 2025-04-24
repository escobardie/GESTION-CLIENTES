from django.views.generic import ListView
from django.views.generic.edit import CreateView
from . import models, forms
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.cliente.models import PromoPorCliente
from django.utils import timezone

def usuario_es_admin(user):
    return user.groups.filter(name='admin').exists()

################# GESTION DE PAGOS ####################
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PagoCreateView(CreateView):
    ''' pago para no clientes '''
    model = models.Pagos
    template_name = 'base/forms/crear_pago.html'
    form_class = forms.PagoForm
    success_url = reverse_lazy('listar_pagos')

    def form_valid(self, form):
        pago = form.save(commit=False)
        pago.cliente = None
        pago.save()
        return super().form_valid(form)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarPagoClienteView(ListView):
    model = models.Pagos
    template_name = "base/listar_pagos_cliente.html"
    paginate_by = 10
    context_object_name = 'lista_pago_cliente'

    def get_cliente_data(self):
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None
    
    def get_queryset(self):
        cliente = self.get_cliente_data()
        return models.Pagos.objects.filter(cliente=cliente)
        

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarPagosView(ListView):
    model = models.Pagos
    template_name = "base/listar_pagos.html"
    paginate_by = 10
    context_object_name = 'lista_pagos'
   
    def get_queryset(self):
        return models.Pagos.objects.all()

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PagoClienteCreateView(CreateView):
    model = models.Pagos
    template_name = 'base/forms/crear_pago_cliente.html'
    form_class = forms.PagoForm
    
    def get_success_url(self):
        id_cliente = self.kwargs.get('id')
        return reverse('menu_cliente', kwargs={'id': id_cliente})

    def get_cliente_data(self):
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None

    # def get_context_data(self, **kwargs): ## ORIGINAL
    #     context = super().get_context_data(**kwargs)
    #     cliente = self.get_cliente_data()

    #     if cliente:
    #         promociones_del_cliente = PromoPorCliente.objects.filter(
    #             cliente=cliente,
    #             estado=True
    #         ).values('promo__id', 'promo__nombre_promo', 'promo__valor_promo', 'promo__vencimiento_promo')
    #         context['promociones'] = promociones_del_cliente
    #     return context
    from django.utils import timezone

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_cliente_data()

        fecha_actual = timezone.now().date()

        if cliente:
            # Obtener las promociones del cliente, incluyendo los datos de Promo relacionados
            promociones_del_cliente = PromoPorCliente.objects.filter(
                cliente=cliente,
                estado=True
            ).select_related('promo')  # Traemos la relación con Promo

            # Inicializamos la lista para almacenar las promociones con su estado
            promociones_con_estado = []
            print(promociones_del_cliente)
            print(fecha_actual)

            for promo_cliente in promociones_del_cliente:
                fecha_vencimiento_promo = promo_cliente.fecha_pago_promo
                print(promo_cliente)
                print(fecha_vencimiento_promo)

                # Comparar la fecha de vencimiento con la fecha actual
                if fecha_vencimiento_promo < fecha_actual:
                    estado_vencimiento = 'VENCIDA'
                else:
                    estado_vencimiento = 'ACTIVA'

                # Agregar la promoción con su estado
                promociones_con_estado.append({
                    'promo_id': promo_cliente.promo.id,
                    'promo_nombre': promo_cliente.promo.nombre_promo,
                    'promo_valor': promo_cliente.promo.valor_promo,
                    'promo_vencimiento': fecha_vencimiento_promo,
                    'estado_vencimiento': estado_vencimiento
                })

            # Pasamos las promociones con su estado al contexto
            context['promociones'] = promociones_con_estado
            

        return context



    def form_valid(self, form):
        cliente = self.get_cliente_data()
        promo_pago_id = self.request.POST.get('promo_id')
        promo_instance = get_object_or_404(models.Promo, id=promo_pago_id)

        fecha_actual = timezone.now().date()

        promo_por_cliente = get_object_or_404(PromoPorCliente, cliente=cliente, promo=promo_instance)

        #print(fecha_actual)
        nueva_fecha_pago = fecha_actual + relativedelta(months=1)
        #print(nueva_fecha_pago)
        promo_por_cliente.fecha_pago_promo = nueva_fecha_pago
        promo_por_cliente.bidones_disponibles = promo_instance.cant_bidones

        promo_por_cliente.save()

        pago = form.save(commit=False)
        pago.cliente = cliente
        pago.promo = promo_instance
        pago.save()
        return super().form_valid(form)
