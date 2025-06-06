from django.shortcuts import render, get_object_or_404, redirect
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
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.usuarios.mixins import ClienteAutorizacionMixin



# def usuario_es_admin(user):
#     return user.groups.filter(name='admin').exists()

# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVentaClienteView(LoginRequiredMixin, ClienteAutorizacionMixin, ListView):
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

# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVentasView(LoginRequiredMixin, ListView): 
    model = models.Venta
    template_name = "base/listar_ventas.html"
    paginate_by = 10
    context_object_name = 'lista_ventas'
    
    # def get_queryset(self):
    #     return models.Venta.objects.all()
    def get_queryset(self):
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        return models.Venta.objects.filter(
            usuario=usuario
        # ).order_by('fecha_venta')
        ).all()


# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class DetalleVentaListView(LoginRequiredMixin, ListView):
    model = models.VentaProducto
    template_name = "base/detalle_venta.html"
    context_object_name = 'detalle_venta'

    def dispatch(self, request, *args, **kwargs):
        ## obtenemos el id de la venta
        self.venta_obj = get_object_or_404(models.Venta, id=self.kwargs['id'])
        ## obtenemos el usuario (dueño) del empleado o subusuario
        usuario_actual = (
            request.user.usuario_padre
            if request.user.rol == 'subusuario'
            else request.user
        )
        ## comparamos el usuario de la venta con el usuario actual (logeado)
        if self.venta_obj.usuario != usuario_actual:
            return redirect('acceso_denegado')
        return super().dispatch(request, *args, **kwargs)

    def get_venta_data(self):
        id_venta = self.kwargs['id']
        venta = get_object_or_404(models.Venta, id=id_venta)
        return venta

    def get_queryset(self):
        venta = self.get_venta_data()
        return models.VentaProducto.objects.filter(venta=venta)


class CrearVentaView(LoginRequiredMixin, CreateView):
    model = models.Venta
    form_class = VentaForm
    template_name = 'base/forms/crear_venta.html'
    # success_url = reverse_lazy('listar_ventas')  # Cambiar por la URL real
    
    #################################
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
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        # context['productos'] = Producto.objects.all() # ORIGINAL
        context['productos'] = Producto.objects.filter(usuario=usuario).all()
        context['nombre_cliente'] = self.get_cliente_data()
        return context
    
    def get_productos_data(self,request):
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        # productos = Producto.objects.all() # ORIGINAL
        productos = Producto.objects.filter(usuario=usuario).all()
        data = {
            producto.id: {
                "precio": str(producto.precio_producto),
                "stock": producto.stock  # Asegúrate de tener este campo en tu modelo
            }
            for producto in productos
        }
        return JsonResponse(data)
    
    def form_valid(self, form):
        cliente = self.get_cliente_data()
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        self.object = form.save(commit=False)
        self.object.usuario = usuario
        self.object.cliente = cliente
        self.object.total_venta = 0
        self.object.save()

        productos_data = self.request.POST.getlist('producto')
        cantidades = self.request.POST.getlist('cantidad')
        descuentos = self.request.POST.getlist('descuento')
        precios = self.request.POST.getlist('precio_unidad')

        nota_venta = self.request.POST.get('nota')
        metodo_pago = self.request.POST.get('metodo_pago')

        for producto_id, cantidad_str, descuento_str, precio_unidad_str in zip(productos_data, cantidades, descuentos, precios):
            cantidad = int(cantidad_str)
            descuento = float(descuento_str)
            precio_unidad = float(precio_unidad_str)

            if cantidad > 0:
                # Buscar el producto y validar stock
                producto = get_object_or_404(models.Producto, id=producto_id)
                if cantidad > producto.stock:
                    form.add_error(None, f"La cantidad para '{producto.nombre_producto}' excede el stock disponible ({producto.stock}).")
                    return self.form_invalid(form)

                # Crear el detalle de venta
                venta_producto = models.VentaProducto.objects.create(
                    usuario= usuario,
                    venta=self.object,
                    producto=producto,
                    cantidad=cantidad,
                    descuento=descuento,
                    precio_unidad_venta=precio_unidad,
                    precio_total_venta=(precio_unidad * cantidad) - descuento,
                )

                # Restar del stock
                producto.stock -= cantidad
                producto.save()

                # Sumar al total de la venta
                self.object.total_venta += venta_producto.precio_total_venta

        self.object.save()

        # 👉 Crear automáticamente el pago
        Pagos.objects.create(
            usuario=usuario,
            venta=self.object, 
            cliente=cliente,
            monto=self.object.total_venta,
            metodo_pago=metodo_pago,
            descripcion=nota_venta
        )

        return super().form_valid(form)


    # def form_valid(self, form):
    #     cliente = self.get_cliente_data()
    #     # Guardar la venta principal
    #     self.object = form.save(commit=False)
    #     self.object.cliente = cliente
    #     self.object.total_venta = 0
    #     self.object.save()

    #     # Procesar productos desde POST
    #     productos_data = self.request.POST.getlist('producto')
    #     cantidades = self.request.POST.getlist('cantidad')
    #     descuentos = self.request.POST.getlist('descuento')
    #     precios = self.request.POST.getlist('precio_unidad')

    #     for producto_id, cantidad, descuento, precio_unidad in zip(productos_data, cantidades, descuentos, precios):
    #         if int(cantidad) > 0:  # Validar que la cantidad sea válida
    #             venta_producto = models.VentaProducto.objects.create(
    #                 venta=self.object,
    #                 producto_id=producto_id,
    #                 cantidad=int(cantidad),
    #                 descuento=float(descuento),
    #                 precio_unidad_venta=float(precio_unidad),
    #                 precio_total_venta=(float(precio_unidad) * int(cantidad)) - float(descuento),
    #             )
    #             self.object.total_venta += venta_producto.precio_total_venta

    #     self.object.save()  # Actualizar el total de la venta
    #     return super().form_valid(form)


# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
## NO ESTA EN USO
# class VentaProductoCreateView(LoginRequiredMixin, FormView):
#     model = models.VentaProducto
#     template_name = 'base/forms/gestion_venta2_fucion.html'
#     # template_name = 'base/forms/cargar_venta_v1.html'
#     form_class = formset_factory(forms.VentaProductoForm)

#     def get_cliente_data(self):
#         cliente_id = self.kwargs.get('id')
#         if cliente_id is not None:
#             return get_object_or_404(models.Cliente, id=cliente_id)
#         return None  

#     def get_success_url(self):
#         cliente_id = self.kwargs.get('id')
#         if cliente_id is not None:
#             return reverse('menu_cliente', kwargs={'id': cliente_id})
#         return reverse('listar_ventas')

#     #################################
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         productos = Producto.objects.filter(
#             estado=True
#         ).values('id', 'nombre_producto', 'precio_producto', 'stock')
#         context['productos'] = productos
#         return context
#     #################################

#     def form_valid(self, form):
#         cliente = self.get_cliente_data()
#         precio_total_todas_venta = self.request.POST.get('precio_total_todas_venta')
#         nota_venta = self.request.POST.get('nota_venta')
#         metodo_pago = self.request.POST.get('metodo_pago')
#         control_stock = self.request.POST.get('descontar_producto')
        
#         if nota_venta == "" and cliente is None:
#             nota_venta = "Venta a No Cliente"      

#         venta = models.Venta.objects.create(
#             cliente=cliente,
#             nota=nota_venta,
#             metodo_pago=metodo_pago,
#             total_venta=precio_total_todas_venta
#         )

#         pago = Pagos.objects.create(
#             cliente=cliente,
#             venta=venta,
#             metodo_pago=metodo_pago,
#             monto=precio_total_todas_venta,
#             descripcion=nota_venta
#         )

#         for f in form:
#             f = f.save(commit=False)
#             f.venta = venta
#             f.save()
#         return super().form_valid(form)
