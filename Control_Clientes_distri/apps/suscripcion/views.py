from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView
from . import models, forms
from django.urls import reverse_lazy

# LoginRequiredMixin
# Propósito: Asegura que el usuario esté autenticado (logueado).

# Uso común: Proteger vistas que solo usuarios registrados pueden ver.

# Redirección automática: Si el usuario no está logueado, se redirige a la URL definida por LOGIN_URL (por defecto: /accounts/login/).

# UserPassesTestMixin
# Propósito: Permite definir una prueba personalizada para determinar si el usuario tiene permiso para ver la vista.

# Se usa junto con test_func(), que tú defines en la vista.

# También redirige si el usuario no pasa la prueba (incluso si está logueado).


class SuscripcionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Suscripcion
    form_class = forms.SuscripcionForm
    template_name = 'base/forms/Crear_suscripcion.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # def handle_no_permission(self):
    #     from django.http import HttpResponseForbidden
    #     return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    def handle_no_permission(self):
        return redirect('acceso_denegado')
    


class CrearSuscripcionPorUsuarioView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.SuscripcionPorUsuario
    form_class = forms.SuscripcionPorUsuarioForm
    template_name = 'base/forms/crear_suscripcion_por_usuario.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    # def handle_no_permission(self):
    #     from django.http import HttpResponseForbidden
    #     return HttpResponseForbidden("No tienes permiso para asignar suscripciones.")
    def handle_no_permission(self):
        return redirect('acceso_denegado')