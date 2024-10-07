from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from . import models, forms
from django.forms import formset_factory
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from datetime import datetime
from dateutil.relativedelta import relativedelta


from django.utils import timezone
from django.contrib import messages

def usuario_es_admin(user):
    return  user.groups.filter(name='admin').exists()
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

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarProductosView(ListView):
    model = models.Producto
    template_name = "Agua/listar_productos.html"
    context_object_name = 'lista_productos'
    paginate_by = 5
    queryset = models.Producto.objects.filter(estado=True).order_by('nombre_producto')

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarClientesView(ListView):
    model = models.Cliente
    template_name = "Agua/listar_clientes.html"
    context_object_name = 'lista_clientes'
    paginate_by = 5
    queryset = models.Cliente.objects.filter(estado=True).order_by('-fecha_alta')

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
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

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVentaClienteView(ListView):
    model = models.Venta
    template_name = "Agua/listar_venta_cliente.html"
    paginate_by = 10
    context_object_name = 'lista_venta_cliente'
    # queryset = models.Venta.objects.filter()

    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id
    
    def get_queryset(self):
        cliente = self.get_cliente_data()
        return models.Venta.objects.filter(cliente=cliente)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarPagoClienteView(ListView):
    model = models.Pagos
    template_name = "Agua/listar_pagos_cliente.html"
    paginate_by = 10
    context_object_name = 'lista_pago_cliente'
    # queryset = models.Venta.objects.filter()

    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id
    
    def get_queryset(self):
        cliente = self.get_cliente_data()
        return models.Pagos.objects.filter(cliente=cliente)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class DetalleVentaListView(ListView):
    model = models.VentaProducto
    template_name = "Agua/detalle_venta.html"
    context_object_name = 'detalle_venta'

    def get_venta_data(self):
        # Obtiene el parámetro 'id' desde los argumentos de la URL.
        # Este 'id' corresponde a una instancia de 'Venta'.
        id_venta = self.kwargs['id']
        
        # Verifica si se proporcionó un 'id_venta'
        if id_venta is not None:
            # Intenta obtener la instancia de 'Venta' asociada con el 'id_venta'.
            # Si no se encuentra, lanza un error 404.
            return get_object_or_404(models.Venta, id=id_venta)
        
        # Si no se proporciona un 'id_venta', devuelve None.
        return None

    def get_queryset(self):
        # Llama al método 'get_venta_data' para obtener la instancia de la 'Venta' correspondiente.
        venta = self.get_venta_data()
        
        # Filtra los objetos 'VentaProducto' asociados con la venta obtenida.
        # Esto devuelve un conjunto de resultados (QuerySet) de productos relacionados con esa venta.
        return models.VentaProducto.objects.filter(venta=venta)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
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

        # Obtén todas las promociones relacionadas con el cliente
        promociones = models.PromoPorCliente.objects.filter(cliente=cliente,estado=True)

        # Crear listas para los datos que se mostrarán
        bidones_disponibles = []
        entrega_bidones = []
        retorno_bidones = []
        bidones_acumulados = []

        for promo in promociones:
            bidones_disponibles.append(promo.bidones_disponibles)
            entrega_bidones.append(promo.entrega_bidones)
            retorno_bidones.append(promo.retorno_bidones)
            bidones_acumulados.append(promo.bidones_acumulados)

        # Agregar la información al contexto
        context['promociones'] = promociones
        context['bidones_disponibles'] = bidones_disponibles
        context['entrega_bidones'] = entrega_bidones
        context['retorno_bidones'] = retorno_bidones
        context['bidones_acumulados'] = bidones_acumulados
        context['promo_asignado'] = promociones.exists()  # Verifica si hay promociones asociadas


        

        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     cliente = self.get_object()  # Obtén el cliente

    #     # Obtén todas las promociones relacionadas con el cliente
    #     promociones = models.PromoPorCliente.objects.filter(cliente=cliente)

        
    #     try:
    #         #promoXcliente = models.PromoPorCliente.objects.get(cliente=cliente)
    #         promoXcliente = models.PromoPorCliente.objects.filter(cliente=cliente)
    #         # context['tipo_promocion'] = cliente.promociones.all() #promoXcliente.promo.nombre_promo
            
    #         context['promociones'] = promoXcliente
    #         # context['bidones_disponibles'] = promoXcliente.bidones_disponibles
    #         # context['entrega_bidones'] = promoXcliente.entrega_bidones
    #         # context['retorno_bidones'] = promoXcliente.retorno_bidones
    #         # context['bidones_acumulados'] = promoXcliente.bidones_acumulados
    #         context['promo_asignado'] = True
            
    #     except models.PromoPorCliente.MultipleObjectsReturned:
    #         # Manejar el caso donde se devuelven múltiples objetos
    #         promoXcliente = models.PromoPorCliente.objects.filter(cliente=cliente)
    #         # Seleccionar el primero, por ejemplo
    #         promoXcliente = promoXcliente.first()
            
    #         # se retorna el nombre de la promocion
    #         # context['tipo_promocion'] = cliente.promociones.all() #promoXcliente.promo.nombre_promo
    #         context['promociones'] = promoXcliente
    #         context['bidones_disponibles'] = promoXcliente.bidones_disponibles
    #         context['entrega_bidones'] = promoXcliente.entrega_bidones
    #         context['retorno_bidones'] = promoXcliente.retorno_bidones
    #         context['bidones_acumulados'] = promoXcliente.bidones_acumulados
    #         context['promo_asignado'] = True

    #     except models.PromoPorCliente.DoesNotExist:
    #         #context['tipo_promocion'] = "No se cargo PROMOCION para este cliente."
    #         context['promociones'] = promociones
    #         context['promo_asignado'] = False
    #         context['bidones_disponibles'] = 0
    #         context['entrega_bidones'] = 0
    #         context['retorno_bidones'] = 0
    #         context['bidones_acumulados'] = 0

                
    #     return context

################# CRUD ####################

## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ClienteCreateView(CreateView):
    model = models.Cliente
    template_name = 'Agua/forms/crear_cliente.html'
    form_class = forms.AddClienteForm
    success_url = reverse_lazy('inicio')
    
   
    def form_valid(self, form):
        form.save()  # Guardar el formulario
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
        cliente_id = self.kwargs.get('id')
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})
    
## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PromoPorClienteCreateView(CreateView):
    template_name = 'Agua/forms/promo_x_cliente.html'
    form_class = forms.AddPromoPorClienteForm

    def get_initial(self):
        # Obtener el cliente específico
        cliente_id = self.kwargs['id']
        # promo_id = self.kwargs['promo_id']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        # promo = get_object_or_404(models.Promo, id=promo_id)
        fecha_actual = datetime.now().date().isoformat()  # 'YYYY-MM-DD'  # Obtiene solo la fecha actual
        # Acceder al campo `cant_bidones` de la instancia de `promo`
        # bidones_disponibles = promo.cant_bidones
        # Retornar los valores iniciales del formulario
        # return {'cliente': cliente, 'promo':promo} # ORIGINAL
        return {
            'cliente': cliente, 
            # 'promo': promo, 
            'inicio_promo': fecha_actual, 
            #'bidones_disponibles': bidones_disponibles
        }

    def form_valid(self, form):
        form.save()  # Guardar el formulario
        return super().form_valid(form)

    def get_success_url(self):
        # Obtiene el ID del cliente desde los kwargs
        cliente_id = self.kwargs.get('id')
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})


@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ServisVisitaUpdateView(UpdateView):
    model = models.PromoPorCliente
    template_name = 'Agua/forms/servis_visita_cliente.html'
    form_class = forms.ServisVisitaClienteForm
    slug_field = 'slug'
    slug_url_kwarg = 'pk'


    def get_object(self):
        cliente_id = self.kwargs.get('pk')
        id_promo = self.request.GET.get('id_promo')  # Obtén el id de la promo de los parámetros GET
        # Busca el objeto usando cliente_id y id_promo
        return get_object_or_404(models.PromoPorCliente, cliente_id=cliente_id, id=id_promo)
    
    def get_cliente_data(self):
        # Obtén el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs['pk']
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente


    def form_valid(self, form):
        cliente = self.get_cliente_data()
        
        promo_id = self.request.GET.get('id_promo')  # Obtén el id de la promo de los parámetros GET
        
        bidones_disponibles = self.request.POST.get('bidones_disponibles')
        entrega_bidones = int(self.request.POST.get('entrega_bidones'))
        retorno_bidones = int(self.request.POST.get('retorno_bidones'))
        bidones_acumulados = self.request.POST.get('bidones_acumulados')
        
        # Actualizar los bidones disponibles en PromoPorCliente
        PromoPorCliente = form.save(commit=False)
        PromoPorCliente.entrega_bidones = 0 
        PromoPorCliente.retorno_bidones = 0
        PromoPorCliente.save()  # Guardar la instancia 


        # Obtener la promoción usando promo_id
        promo = get_object_or_404(models.PromoPorCliente, id=promo_id)

        # Crear una nueva instancia de Visita y guardar
        visita = models.Visita.objects.create(
            cliente=cliente,
            nota="<ul>"+
                    f"<li>PROMOCION:  {promo.promo.nombre_promo}</li>"+
                    f"<li>BIDONES DISPONIBLES:  {bidones_disponibles}</li>"+
                    f"<li>BIDONES ENTREGADOS AL CLIENTE: {entrega_bidones} </li>"+
                    f"<li>BIDONES RETIRADOS DEL DOMICILIO:{retorno_bidones}</li>"+
                    f"<li>BIDONES EN PODER DEL CLIENTE: {bidones_acumulados}</li>"+
                "</ul>"
        )

        return super().form_valid(form)

    def get_success_url(self):
        # Obtiene el ID del cliente desde los kwargs
        cliente_id = self.kwargs.get('pk')
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})


################# GESTION DE LAS VENTAS ####################
## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ProductoCreateView(CreateView):
    model = models.Producto
    template_name = 'Agua/forms/crear_producto.html'
    form_class = forms.ProductoForm
    success_url = reverse_lazy('inicio')
    
   
    def form_valid(self, form):
        form.save()  # Guardar el formulario
        return super().form_valid(form)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VentaCreateView(CreateView): ##TODO CORROBORAR SI SE USA TODAVIA
    model = models.Venta
    template_name = 'Agua/forms/crear_venta.html'
    form_class = forms.VentaForm
    success_url = reverse_lazy('inicio')
    
   
    def form_valid(self, form):
        form.save()  # Guardar el formulario
        return super().form_valid(form)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VentaProductoCreateView2(CreateView): ##TODO CORROBORAR SI SE USA TODAVIA
    model = models.VentaProducto
    template_name = 'Agua/forms/crear_venta_producto.html'
    form_class = forms.VentaProductoForm
    success_url = reverse_lazy('inicio')
    
   
    def form_valid(self, form):
        form.save()  # Guardar el formulario
        return super().form_valid(form)

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class GestioVentaView(CreateView): ##TODO CORROBORAR SI SE USA TODAVIA
    model = models.VentaProducto
    template_name = 'Agua/forms/gestion_venta2.html'
    form_class = forms.VentaProductoForm
    success_url = reverse_lazy('inicio')
    
    def form_invalid(self, form): ## NO BORRAR
        print("Formulario inválido:", form.errors)
        return super().form_invalid(form)

    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id
        
    def form_valid(self, form):
        cliente = self.get_cliente_data()
        # Crear una nueva instancia de Venta y guardar
        venta = models.Venta.objects.create(cliente=cliente)
        ##################
         # Procesar productos
        producto_list = self.request.POST.getlist('producto')
        producto=form.cleaned_data['producto']
        cantidad_list = self.request.POST.getlist('cantidad')
        descuento_list = self.request.POST.getlist('descuento')
        precio_list = self.request.POST.getlist('precio_unidad_venta')
        precio_total_venta_list = self.request.POST.getlist('precio_total_venta')
        print("PROBANDO 1")
        print(producto_list)
        print(producto)
        print("PROBANDO 2")
        print(cantidad_list)
        print(descuento_list)
        print(precio_list)
        print(precio_total_venta_list)
        ##################
        # Ahora guarda la instancia de VentaProducto asociándola a la venta creada
        venta_producto = form.save(commit=False)
        venta_producto.venta = venta  # Asocia la venta a VentaProducto
        venta_producto.save()  # Ahora guarda el VentaProducto

        # form.save()  # Guardar el formulario
        return super().form_valid(form)

class VentaProductoCreateView(FormView):
    ## https://www.youtube.com/watch?v=fycZ_d2vDwM
    ## https://github.com/neunapp/formsets-django/blob/master/djfomrsets/templates/alumno/add.html
    model = models.VentaProducto
    template_name = 'Agua/forms/gestion_venta2_fucion.html'
    ## formset_factory = conjunto de formularios
    form_class = formset_factory(forms.VentaProductoForm)
    success_url = reverse_lazy('inicio')

    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id

    def form_valid(self, form):
        cliente = self.get_cliente_data()
        # Captura el valor de precio_total_todas_venta
        precio_total_todas_venta = self.request.POST.get('precio_total_todas_venta')
        nota_venta = self.request.POST.get('nota_venta')
        
        if nota_venta == "" and cliente == None:
            nota_venta = "Venta a No Cliente"      

        # Crear una nueva instancia de Venta y guardar
        venta = models.Venta.objects.create(
            cliente=cliente,
            nota= nota_venta,
            total_venta=precio_total_todas_venta
            )

        # Crear una nueva instancia de PAGO y guardar
        pago = models.Pagos.objects.create(
            cliente=cliente,
            venta=venta,
            monto=precio_total_todas_venta,
            descripcion=nota_venta
        )

        for f in form:
            # Ahora guarda la instancia de VentaProducto asociándola a la venta creada
            f = f.save(commit=False)
            f.venta = venta  # Asocia la venta a VentaProducto
            f.save()  # Guardar el formulario
        return super().form_valid(form)
################# GESTION DE LAS VENTAS ####################


################# GESTION DE PAGOS ####################
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PagoCreateView(CreateView):
    model = models.Pagos
    template_name = 'Agua/forms/crear_pago.html'
    form_class = forms.PagoForm
    success_url = reverse_lazy('inicio')
    
    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id

    def form_valid(self, form):
        cliente = self.get_cliente_data()
        pago = form.save(commit=False)
        pago.cliente = cliente
        pago.save()  # Guardar el formulario
        return super().form_valid(form)


@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PagoClienteCreateView(CreateView):
    model = models.Pagos
    template_name = 'Agua/forms/crear_pago_cliente.html'
    form_class = forms.PagoForm
    success_url = reverse_lazy('inicio')
    
    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id
    
    # def  get_context_data(self, **kwargs): ##filtra todos los PROMOS del cliente
    #     context = super().get_context_data(**kwargs)
    #     cliente = self.get_cliente_data()
    #     # Filtrar los promos cuyo estado asociadas con el cliente
    #     promociones_del_cliente = models.PromoPorCliente.objects.filter(cliente=cliente,estado=True)
    #     # Crear listas para los datos que se mostrarán
    #     lista_promo_del_cliente = []
    #     # for promo in promociones_del_cliente:
    #     #     lista_promo_del_cliente.append(promo.promo.nombre_promo)
        
    #     for promo in promociones_del_cliente:
    #         lista_promo_del_cliente.append({
    #             'nombre': promo.promo.nombre_promo,
    #             'precio': promo.promo.valor_promo,  
    #             'fecha': promo.promo.vencimiento_promo 
    #         })

    #     # Agregar la información al contexto
    #     context['promociones'] = lista_promo_del_cliente
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_cliente_data()
        '''  En lugar de construir el diccionario a mano, 
            podrías usar values() o values_list() si solo necesitas ciertos campos,
            lo que optimizaría la consulta a la base de datos. '''

        if cliente:
            # Filtrar las promociones activas del cliente
            promociones_del_cliente = models.PromoPorCliente.objects.filter(
                cliente=cliente,
                estado=True
            ).values('promo__id','promo__nombre_promo', 'promo__valor_promo', 'promo__vencimiento_promo')
            context['promociones'] = promociones_del_cliente
        return context

    def form_valid(self, form):
        cliente = self.get_cliente_data()
        promo_pago_id = self.request.POST.get('promo_id') # Captura el promo__id
        promo_instance = get_object_or_404(models.Promo, id=promo_pago_id)

        # Obtener la instancia de PromoPorCliente asociada al cliente y promoción
        promo_por_cliente = get_object_or_404(models.PromoPorCliente, cliente=cliente, promo=promo_instance)

        ## Actualizar la fecha de pago
        nueva_fecha_pago = (datetime.now() + relativedelta(months=1)).date().isoformat()  # Sumar 1 mes a la fecha actual
        promo_por_cliente.fecha_pago_promo = nueva_fecha_pago
        promo_por_cliente.bidones_disponibles = promo_instance.cant_bidones

        # Guardar cambios en PromoPorCliente
        promo_por_cliente.save()

        
        
        pago = form.save(commit=False)
        pago.cliente = cliente
        pago.promo = promo_instance
        pago.save()  # Guardar el formulario
        return super().form_valid(form)