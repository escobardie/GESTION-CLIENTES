from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . import models, forms

def usuario_es_admin(user):
    return user.groups.filter(name='admin').exists()

@method_decorator(user_passes_test(usuario_es_admin, login_url='inicio'), name='dispatch')
class PromoCreateView(CreateView):
    model = models.Promo
    form_class = forms.AddPromoForm
    template_name = 'Agua/forms/crear_promo.html'
    success_url = reverse_lazy('inicio')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
