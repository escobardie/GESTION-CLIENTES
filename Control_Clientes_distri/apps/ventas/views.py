from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, FormView
from django.forms import formset_factory
from django.urls import reverse, reverse_lazy
from . import models, forms
from apps.pagos.models import Pagos
from apps.productos.models import Producto
from .forms import VentaForm, VentaProductoFormSet
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.http import JsonResponse


def usuario_es_admin(user):
    return user.groups.filter(name='admin').exists()

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVentaClienteView(ListView):
    model = models.Venta
    template_name = "base/listar_venta_cliente.html"
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
class ListarVentasView(ListView): 
    model = models.Venta
    template_name = "base/listar_ventas.html"
    paginate_by = 10
    context_object_name = 'lista_ventas'
    
    def get_queryset(self):
        return models.Venta.objects.all()

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class DetalleVentaListView(ListView):
    model = models.VentaProducto
    template_name = "base/detalle_venta.html"
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
    template_name = 'base/forms/gestion_venta2_fucion.html'
    # template_name = 'base/forms/cargar_venta_v1.html'
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

    #################################
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productos = Producto.objects.filter(
            estado=True
        ).values('id', 'nombre_producto', 'precio_producto', 'stock')
        context['productos'] = productos
        return context
    #################################

    def form_valid(self, form):
        cliente = self.get_cliente_data()
        precio_total_todas_venta = self.request.POST.get('precio_total_todas_venta')
        nota_venta = self.request.POST.get('nota_venta')
        metodo_pago = self.request.POST.get('metodo_pago')
        control_stock = self.request.POST.get('descontar_producto')
        
        if nota_venta == "" and cliente is None:
            nota_venta = "Venta a No Cliente"      

        venta = models.Venta.objects.create(
            cliente=cliente,
            nota=nota_venta,
            metodo_pago=metodo_pago,
            total_venta=precio_total_todas_venta
        )

        pago = Pagos.objects.create(
            cliente=cliente,
            venta=venta,
            metodo_pago=metodo_pago,
            monto=precio_total_todas_venta,
            descripcion=nota_venta
        )

        for f in form:
            f = f.save(commit=False)
            f.venta = venta
            f.save()
        return super().form_valid(form)



class CrearVentaView(CreateView):
    model = models.Venta
    form_class = VentaForm
    template_name = 'base/forms/crear_venta.html'
    success_url = reverse_lazy('listar_ventas')  # Cambiar por la URL real

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()  # Enviar productos al template
        return context
    
    def get_productos_data(request):
        productos = Producto.objects.all()
        data = {
            producto.id: {
                "precio": str(producto.precio_producto),
                "stock": producto.stock  # Asegúrate de tener este campo en tu modelo
            }
            for producto in productos
        }
        return JsonResponse(data)

    def form_valid(self, form):
        # Guardar la venta principal
        self.object = form.save(commit=False)
        self.object.total_venta = 0
        self.object.save()

        # Procesar productos desde POST
        productos_data = self.request.POST.getlist('producto')
        cantidades = self.request.POST.getlist('cantidad')
        descuentos = self.request.POST.getlist('descuento')
        precios = self.request.POST.getlist('precio_unidad')

        for producto_id, cantidad, descuento, precio_unidad in zip(productos_data, cantidades, descuentos, precios):
            if int(cantidad) > 0:  # Validar que la cantidad sea válida
                venta_producto = models.VentaProducto.objects.create(
                    venta=self.object,
                    producto_id=producto_id,
                    cantidad=int(cantidad),
                    descuento=float(descuento),
                    precio_unidad_venta=float(precio_unidad),
                    precio_total_venta=(float(precio_unidad) * int(cantidad)) - float(descuento),
                )
                self.object.total_venta += venta_producto.precio_total_venta

        self.object.save()  # Actualizar el total de la venta
        return super().form_valid(form)