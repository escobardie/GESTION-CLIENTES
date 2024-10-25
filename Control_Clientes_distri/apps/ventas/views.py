from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, FormView
from django.forms import formset_factory
from django.urls import reverse
from . import models, forms
from apps.pagos.models import Pagos

def usuario_es_admin(user):
    return user.groups.filter(name='admin').exists()

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVentaClienteView(ListView):
    model = models.Venta
    template_name = "Agua/listar_venta_cliente.html"
    paginate_by = 10
    context_object_name = 'lista_venta_cliente'

    def get_cliente_data(self):
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None
    
    def get_queryset(self):
        cliente = self.get_cliente_data()
        return models.Venta.objects.filter(cliente=cliente)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class DetalleVentaListView(ListView):
    model = models.VentaProducto
    template_name = "Agua/detalle_venta.html"
    context_object_name = 'detalle_venta'

    def get_venta_data(self):
        id_venta = self.kwargs['id']
        venta = get_object_or_404(models.Venta, id=id_venta)
        return venta

    def get_queryset(self):
        venta = self.get_venta_data()
        return models.VentaProducto.objects.filter(venta=venta)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VentaProductoCreateView(FormView):
    model = models.VentaProducto
    template_name = 'Agua/forms/gestion_venta2_fucion.html'
    form_class = formset_factory(forms.VentaProductoForm)

    def get_cliente_data(self):
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  

    def get_success_url(self):
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return reverse('menu_cliente', kwargs={'id': cliente_id})
        return reverse('listar_ventas')

    def form_valid(self, form):
        cliente = self.get_cliente_data()
        precio_total_todas_venta = self.request.POST.get('precio_total_todas_venta')
        nota_venta = self.request.POST.get('nota_venta')
        
        if nota_venta == "" and cliente is None:
            nota_venta = "Venta a No Cliente"      

        venta = models.Venta.objects.create(
            cliente=cliente,
            nota=nota_venta,
            total_venta=precio_total_todas_venta
        )

        pago = Pagos.objects.create(
            cliente=cliente,
            venta=venta,
            monto=precio_total_todas_venta,
            descripcion=nota_venta
        )

        for f in form:
            f = f.save(commit=False)
            f.venta = venta
            f.save()
        return super().form_valid(form)
