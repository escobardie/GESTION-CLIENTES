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
    model = models.PromoPorCliente
    template_name = "Agua/index.html"
    context_object_name = "listar_promos"
    paginate_by = 10

    def get_queryset(self):
        # Filtrar las promociones cuyo estado es True y ordenar por fecha pago
        return models.PromoPorCliente.objects.filter(estado=True).order_by('fecha_pago_promo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el queryset filtrado
        queryset = self.get_queryset()
        # Obtener la fecha actual
        fecha_actual = timezone.now().date()
        # Filtrar promociones con fecha de pago vencida
        promo_con_fecha_vencida = queryset.filter(fecha_pago_promo__lt=fecha_actual)
        # Pasar esta información al contexto
        context['promos_con_fecha_vencida'] = promo_con_fecha_vencida
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
    queryset = models.Cliente.objects.filter(estado=True).order_by('apellido')

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVisitasView(ListView):
    model = models.Visita
    template_name = "Agua/listar_vistas.html"
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

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarVentaClienteView(ListView):
    model = models.Venta
    template_name = "Agua/listar_venta_cliente.html"
    paginate_by = 10
    context_object_name = 'lista_venta_cliente'

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
        ## NO PUEDE EXISTIR UN NONE COMO ID DE DETALLE VENTA
        # Obtiene el parámetro 'id' desde los argumentos de la URL.
        id_venta = self.kwargs['id']
        venta = get_object_or_404(models.Venta, id=id_venta)
        return venta

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
        ## NO PUEDE EXISTIR UN NONE COMO ID DE CLIENTE
        # Obtén el parámetro 'id' desde la URL
        cliente_id = self.kwargs['id']
        # Busca el cliente por su 'id'. Si no se encuentra, arroja un error 404.
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return cliente
    ## CODIGO EXTRA SIN USO, PERO PARA FUTURAS REFERENCIAS
        # def get_context_data(self, **kwargs):
        #     context = super().get_context_data(**kwargs)
        #     cliente = self.get_object()  # Obtén el cliente

        #     # Obtén todas las promociones relacionadas con el cliente
        #     promociones = models.PromoPorCliente.objects.filter(cliente=cliente,estado=True)

        #     ### NUEVO ENFOQUE ###
        #     # # Crear listas para los datos que se mostrarán
        #     # lista_detalles_promo_cliente = []
            
        #     # for promo in promociones:
        #     #     lista_detalles_promo_cliente.append({
        #     #         'bidones_disponibles': promo.bidones_disponibles,
        #     #         'entrega_bidones': promo.entrega_bidones,
        #     #         'retorno_bidones': promo.retorno_bidones,
        #     #         'bidones_acumulados': promo.bidones_acumulados 
        #     #     })

        #     # # Agregar la información al contexto
        #     # context['promociones'] = lista_detalles_promo_cliente
        #     # context['promo_asignado'] = promociones.exists()  # Verifica si hay promociones asociadas
        #     ### NUEVO ENFOQUE ###

        #     # Crear listas para los datos que se mostrarán
        #     bidones_disponibles = []
        #     entrega_bidones = []
        #     retorno_bidones = []
        #     bidones_acumulados = []

        #     for promo in promociones:
        #         bidones_disponibles.append(promo.bidones_disponibles)
        #         entrega_bidones.append(promo.entrega_bidones)
        #         retorno_bidones.append(promo.retorno_bidones)
        #         bidones_acumulados.append(promo.bidones_acumulados)

        #     # Agregar la información al contexto
        #     context['promociones'] = promociones
        #     context['bidones_disponibles'] = bidones_disponibles
        #     context['entrega_bidones'] = entrega_bidones
        #     context['retorno_bidones'] = retorno_bidones
        #     context['bidones_acumulados'] = bidones_acumulados
        #     context['promo_asignado'] = promociones.exists()  # Verifica si hay promociones asociadas

        #     return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        '''  En lugar de construir el diccionario a mano, 
            usamos values() o values_list() si solo hace falta ciertos campos,
            lo que optimizaría la consulta a la base de datos. '''

        if cliente:
            # Filtrar las promociones activas del cliente
            promociones_del_cliente = models.PromoPorCliente.objects.filter(
                cliente=cliente,
                estado=True
            ).values('id','promo__nombre_promo','promo__valor_promo',
            'fecha_pago_promo', 'bidones_disponibles', 'bidones_acumulados')
            context['promociones'] = promociones_del_cliente
        return context
    

################# CRUD ####################
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PromoCreateView(CreateView):
    model = models.Promo
    form_class = forms.AddPromoForm
    template_name = 'Agua/forms/crear_promo.html'
    success_url = reverse_lazy('inicio')
    
    def form_valid(self, form):
        form.save()  # Guardar el formulario
        return super().form_valid(form)

## se agrega capa de seguridad para la carga de datos
@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ClienteCreateView(CreateView): 
    ''' FORMULARIO BASICO '''
    model = models.Cliente
    template_name = 'Agua/forms/crear_cliente.html'
    form_class = forms.AddClienteForm
    # success_url = reverse_lazy('inicio')
    def get_success_url(self):
        # Redirigir al menú del cliente creado
        return reverse('menu_cliente', kwargs={'id': self.object.id})
   
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
        cliente_id = self.kwargs.get('id') ## USAMOS ESTE PORQUE EL USAMOS EL FORMULARIO PREDETERMIANDO "{{ form.as_p }}"
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
        cliente = get_object_or_404(models.Cliente, id=cliente_id)
        return {'cliente': cliente}

    def form_valid(self, form):
        promo_id = form.cleaned_data['promo'].id  # Obtén el ID de promo
        promo_instance = get_object_or_404(models.Promo, id=promo_id)

        fecha_actual = datetime.now().date().isoformat()  # 'YYYY-MM-DD'  # Obtiene solo la fecha actual
        dibones_disponibles_promo = promo_instance.cant_bidones
        promocliente = form.save(commit=False)
        promocliente.inicio_promo = fecha_actual
        promocliente.bidones_disponibles = dibones_disponibles_promo
        promocliente.save()  # Guardar el formulario
        return super().form_valid(form)

    def get_success_url(self):
        # Obtiene el ID del cliente desde los kwargs
        cliente_id = self.kwargs.get('id')
        # Genera la URL para la vista 'menu_cliente' usando el ID del cliente
        return reverse('menu_cliente', kwargs={'id': cliente_id})


@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ServisVisitaUpdateView(UpdateView): ## TODO realizar chequeo con el cliente
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
    success_url = reverse_lazy('listar_productos')
    
   
    def form_valid(self, form):
        form.save()  # Guardar el formulario
        return super().form_valid(form)


@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class VentaProductoCreateView(FormView):
    ## https://www.youtube.com/watch?v=fycZ_d2vDwM
    ## https://github.com/neunapp/formsets-django/blob/master/djfomrsets/templates/alumno/add.html
    model = models.VentaProducto
    template_name = 'Agua/forms/gestion_venta2_fucion.html'
    ## formset_factory = conjunto de formularios
    form_class = formset_factory(forms.VentaProductoForm)
    # success_url = reverse_lazy('inicio')

    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id

    def get_success_url(self):
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return reverse('menu_cliente', kwargs={'id': cliente_id})
        return reverse('listar_ventas')

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
    ''' pago para no clientes '''
    model = models.Pagos
    template_name = 'Agua/forms/crear_pago.html'
    form_class = forms.PagoForm
    success_url = reverse_lazy('listar_pago')

    def form_valid(self, form):
        pago = form.save(commit=False)
        pago.cliente = None
        pago.save()  # Guardar el formulario
        return super().form_valid(form)


@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PagoClienteCreateView(CreateView):
    model = models.Pagos
    template_name = 'Agua/forms/crear_pago_cliente.html'
    form_class = forms.PagoForm
    # success_url = reverse_lazy('inicio')
    
    def get_success_url(self): ## FUNCIONA PERFECTO
        # Obtiene el ID
        id_cliente = self.kwargs.get('id')
        # Genera la URL para la vista 'MENU CLIENTE' usando el ID
        return reverse('menu_cliente', kwargs={'id': id_cliente})


    def get_cliente_data(self):
        # Intenta obtener el cliente_id de los argumentos de la URL
        cliente_id = self.kwargs.get('id')
        if cliente_id is not None:
            return get_object_or_404(models.Cliente, id=cliente_id)
        return None  # Devuelve None si no hay cliente_id

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

        # Capturar la fecha de pago de la promoción actual
        fecha_pago_promo = promo_por_cliente.fecha_pago_promo

        # Sumar un mes a la fecha de pago actual
        nueva_fecha_pago = fecha_pago_promo + relativedelta(months=1)

        promo_por_cliente.fecha_pago_promo = nueva_fecha_pago
        promo_por_cliente.bidones_disponibles = promo_instance.cant_bidones

        # Guardar cambios en PromoPorCliente
        promo_por_cliente.save()

        
        
        pago = form.save(commit=False)
        pago.cliente = cliente
        pago.promo = promo_instance
        pago.save()  # Guardar el formulario
        return super().form_valid(form)