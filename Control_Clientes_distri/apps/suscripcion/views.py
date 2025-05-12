from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView 
from . import models, forms
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from django.http import JsonResponse
from django.views import View
from django.utils.timezone import now
from apps.suscripcion.models import SuscripcionPorUsuario

import qrcode
import base64
from io import BytesIO
from django.utils.html import mark_safe
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from apps.usuarios.models import Usuario
from apps.usuarios.forms import UsuarioForm

# LoginRequiredMixin
# Propósito: Asegura que el usuario esté autenticado (logueado).

# Uso común: Proteger vistas que solo usuarios registrados pueden ver.

# Redirección automática: Si el usuario no está logueado, se redirige a la URL definida por LOGIN_URL (por defecto: /accounts/login/).

# UserPassesTestMixin
# Propósito: Permite definir una prueba personalizada para determinar si el usuario tiene permiso para ver la vista.

# Se usa junto con test_func(), que tú defines en la vista.

# También redirige si el usuario no pasa la prueba (incluso si está logueado).
def generar_qr_base64(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def recibo_pdf_view(request, token):
    pago = get_object_or_404(models.PagoSuscriptor, token=token)
    template = get_template('tickets/pago/suscripcion/recibo_pago_pdf.html')
    html = template.render({'pago': pago})

    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=recibo_{pago.token}.pdf'
    return response


class CrearSuscriptorView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'base/forms/crear_usuario_suscriptor.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser 

    def handle_no_permission(self):
        return redirect('acceso_denegado')
    
    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.rol = 'cliente'
        usuario.save()  # Guardar el formulario
        return super().form_valid(form)
    


class ObtenerSuscripcionDeUsuarioView(View): ##TODO: ESTE ENFOQUE GENERADO CON CHAT ES MEJOR QUE EL MIO :(
    def get(self, request, *args, **kwargs):
        usuario_id = request.GET.get('usuario_id')

        try:
            usuario = Usuario.objects.get(id=usuario_id, rol='cliente')
            relacion = SuscripcionPorUsuario.objects.get(usuario=usuario)

            suscripcion = relacion.suscripcion
            activa = relacion.estado and relacion.fecha_fin_suscrip >= now().date()

            return JsonResponse({
                'id': suscripcion.id,
                'nombre': suscripcion.nombre_suscripcion,
                'estado': 'activa' if activa else 'expirada',
                'fecha_fin': relacion.fecha_fin_suscrip.strftime('%Y-%m-%d'),
                'monto': str(suscripcion.valor_suscripcion),  # como string para evitar problemas de formato
            })

        except (Usuario.DoesNotExist, SuscripcionPorUsuario.DoesNotExist):
            return JsonResponse({}, status=404)


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
    

# class RegistrarPagoSuscriptorView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = models.PagoSuscriptor
#     form_class = forms.PagoSuscriptorForm
#     template_name = 'base/forms/registrar_pago_suscriptor.html'
#     success_url = reverse_lazy('lista_pagos')  # Cámbialo a la URL que desees redireccionar

#     def test_func(self):
#         # Solo usuarios staff/superuser pueden registrar pagos
#         return self.request.user.is_staff or self.request.user.is_superuser

#     # def handle_no_permission(self):
#     #     from django.http import HttpResponseForbidden
#     #     return HttpResponseForbidden("No tienes permiso para registrar pagos.")
#     def handle_no_permission(self):
#         return redirect('acceso_denegado')

class RegistrarPagoSuscriptorView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.PagoSuscriptor
    form_class = forms.PagoSuscriptorForm
    template_name = 'base/forms/registrar_pago_suscriptor.html'
    success_url = reverse_lazy('lista_pagos')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('acceso_denegado')

    def form_valid(self, form):
        usuario = form.cleaned_data['usuario']
        try:
            relacion = usuario.suscripcion_asociada
            if not relacion.estado or relacion.fecha_fin_suscrip < now().date():
                form.add_error(None, "El usuario no tiene una suscripción activa.")
                return self.form_invalid(form)

            form.instance.suscripcion = relacion.suscripcion
            form.instance.monto = relacion.suscripcion.valor_suscripcion

        except SuscripcionPorUsuario.DoesNotExist:
            form.add_error(None, "El usuario no tiene una suscripción asignada.")
            return self.form_invalid(form)

        return super().form_valid(form)



class ListaPagosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = models.PagoSuscriptor
    template_name = 'base/lista_pagos_suscriptor.html'
    context_object_name = 'pagos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario = self.request.GET.get('usuario')
        metodo_pago = self.request.GET.get('metodo_pago')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')

        if usuario:
            queryset = queryset.filter(usuario__username__icontains=usuario)
        if metodo_pago:
            queryset = queryset.filter(metodo_pago=metodo_pago)
        if fecha_desde:
            queryset = queryset.filter(fecha_pago__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_pago__date__lte=fecha_hasta)

        return queryset
    
    def test_func(self):
        # Solo usuarios staff/superuser pueden registrar pagos
        return self.request.user.is_staff or self.request.user.is_superuser

    # def handle_no_permission(self):
    #     from django.http import HttpResponseForbidden
    #     return HttpResponseForbidden("No tienes permiso para registrar pagos.")
    def handle_no_permission(self):
        return redirect('acceso_denegado')



class ReciboPagoImprimibleView(DetailView):
    model = models.PagoSuscriptor
    template_name = 'tickets/pago/suscripcion/recibo_pago.html'
    context_object_name = 'pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pago = self.object

        # Construir URL absoluta del recibo
        recibo_url = self.request.build_absolute_uri(
            reverse('recibo_pago', kwargs={'pk': pago.pk})
        )

        # Generar QR con la URL
        qr_b64 = generar_qr_base64(recibo_url)

        context['qr_base64'] = mark_safe(f"data:image/png;base64,{qr_b64}")
        context['recibo_url'] = recibo_url

        context['mensaje'] = (
            f"Hola {pago.usuario.username}, "
            f"gracias por tu pago de ${pago.monto} correspondiente a tu suscripción "
            f"'{pago.suscripcion.nombre_suscripcion}'. "
            f"Aquí tienes tu recibo: {self.request.build_absolute_uri(self.request.path)}"
        )
        return context

class ReciboPagoConTokenView(DetailView):
    model = models.PagoSuscriptor
    template_name = 'tickets/pago/suscripcion/recibo_pago.html'
    context_object_name = 'pago'

    def get_object(self, queryset=None):
        token = self.kwargs.get('token')
        return get_object_or_404(models.PagoSuscriptor, token=token)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pago = self.object

        recibo_url = self.request.build_absolute_uri(self.request.path)
        qr_b64 = generar_qr_base64(recibo_url)

        context['qr_base64'] = mark_safe(f"data:image/png;base64,{qr_b64}")
        context['recibo_url'] = recibo_url

        recibo_url = self.request.build_absolute_uri(
            reverse('recibo_pago_token', kwargs={'token': pago.token})
        )
        pdf_url = self.request.build_absolute_uri(
            reverse('recibo_pago_pdf', kwargs={'token': pago.token})
        )

        context['recibo_url'] = recibo_url
        context['pdf_url'] = pdf_url

        context['mensaje'] = (
            f"Hola {pago.usuario.username}, gracias por tu pago de ${pago.monto}. "
            f"Puedes ver tu recibo aquí: {recibo_url} o descargarlo en PDF: {pdf_url}"
        )


        return context


