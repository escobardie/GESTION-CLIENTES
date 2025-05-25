from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin

# def usuario_es_admin(user):
#     return user.groups.filter(name='admin').exists()

################# GESTION DE LAS VENTAS ####################
## se agrega capa de seguridad para la carga de datos
# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = models.Producto
    template_name = 'Base/forms/crear_producto.html'
    form_class = forms.ProductoForm
    success_url = reverse_lazy('listar_productos')

    # def form_valid(self, form):
    #     form.save()  # Guardar el formulario
    #     return super().form_valid(form)
    
    def form_valid(self, form):
        # Si es subusuario, usar su cliente asociado
        usuario_asociado = (
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        form.instance.usuario = usuario_asociado
        return super().form_valid(form)

# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class ListarProductosView(LoginRequiredMixin, ListView):
    model = models.Producto
    template_name = "Base/listar_productos.html"
    context_object_name = 'lista_productos'
    paginate_by = 5
    # queryset = models.Producto.objects.filter(estado=True).order_by('nombre_producto')
    
    def get_queryset(self):
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        return models.Producto.objects.filter(
            estado=True,
            usuario=usuario
        ).order_by('nombre_producto')