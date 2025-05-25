from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin

# def usuario_es_admin(user):
#     return user.groups.filter(name='admin').exists()

# @method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PromoCreateView(LoginRequiredMixin, CreateView):
    model = models.Promo
    form_class = forms.AddPromoForm
    template_name = 'Base/forms/crear_promo.html'
    success_url = reverse_lazy('listar_promociones')
    
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
class ListarPromocionesView(LoginRequiredMixin, ListView):
    model = models.Promo
    template_name = "Base/listar_promociones.html"
    context_object_name = 'lista_promos'
    paginate_by = 5
    # queryset = models.Promo.objects.filter(estado=True).order_by('nombre_promo') # ya no se usa

    def get_queryset(self):
        usuario = (
            # Si es subusuario, usar su cliente asociado
            self.request.user.usuario_padre
            if self.request.user.rol == 'subusuario'
            else self.request.user
        )
        return models.Promo.objects.filter(
            estado=True,
            usuario=usuario
        ).order_by('nombre_promo')