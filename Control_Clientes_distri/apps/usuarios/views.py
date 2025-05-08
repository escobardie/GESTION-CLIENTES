# views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from .forms import SubusuarioForm
from . import models, forms
from django.contrib import messages  # Importamos para enviar mensajes al usuario
from django.shortcuts import get_object_or_404

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.views.generic import TemplateView



Usuario = get_user_model()


class LoginPersonalizadoView(LoginView):
    template_name = 'User/login.html'  # template personalizado
    redirect_authenticated_user = True  # Si ya está logueado, redirige automáticamente

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin/'
        elif user.rol == 'cliente':
            return reverse_lazy('listar_ventas')
        elif user.rol == 'subusuario':
            return reverse_lazy('listar_vto_clte')
        else:
            return reverse_lazy('index')  # fallback por si acaso
        
# class LogoutView(DjangoLogoutView):
#     def get_next_page(self):
#         return reverse_lazy('login')

class AccesoDenegadoView(TemplateView):
    template_name = 'errors/acceso_denegado.html'


# @login_required
# def crear_subusuario(request):
#     if not request.user.es_cliente():
#         return redirect('index')  # o un error 403

#     if request.method == 'POST':
#         form = forms.SubusuarioForm(request.POST)
#         if form.is_valid():
#             subusuario = form.save(commit=False)
#             subusuario.rol = 'subusuario'
#             subusuario.cliente = request.user  # Lo asignamos al cliente actual
#             subusuario.set_password(form.cleaned_data['password'])  # Para que la contraseña quede hasheada
#             subusuario.save()
#             return redirect('listado_subusuarios')  # o a donde quieras ir después
#     else:
#         form = forms.SubusuarioForm()

#     return render(request, 'crear_subusuario.html', {'form': form})

# from django.contrib import messages  # Importamos para enviar mensajes al usuario

@login_required
def crear_subusuario(request):
    if not request.user.es_cliente():
        return redirect('index')  # o un error 403

    # 🔥 Límite de subusuarios (acá seteamos el límite)
    LIMITE_SUBUSUARIOS = 2

    # Contar subusuarios actuales
    cantidad_subusuarios = request.user.empleados.count()

    if cantidad_subusuarios >= LIMITE_SUBUSUARIOS:
        messages.error(request, "Has alcanzado el límite máximo de subusuarios.")
        return redirect('listado_subusuarios')  # o donde quieras redirigir si ya no puede crear más

    if request.method == 'POST':
        form = forms.SubusuarioForm(request.POST)
        if form.is_valid():
            subusuario = form.save(commit=False)
            subusuario.rol = 'subusuario'
            subusuario.cliente = request.user
            subusuario.set_password(form.cleaned_data['password'])
            subusuario.save()
            messages.success(request, "Subusuario creado exitosamente.")
            return redirect('listado_subusuarios')
    else:
        form = forms.SubusuarioForm()

    return render(request, 'base/forms/crear_subusuario.html', {'form': form})

@login_required
def listar_subusuarios(request):
    if not request.user.es_cliente():
        return redirect('index')  # o error 403

    subusuarios = request.user.empleados.all()  # Todos los empleados del cliente

    return render(request, 'base/listar_subusuarios.html', {'subusuarios': subusuarios})


@login_required
def editar_subusuario(request, subusuario_id):
    if not request.user.es_cliente():
        return redirect('inicio')

    subusuario = get_object_or_404(request.user.empleados, id=subusuario_id)

    if request.method == 'POST':
        form = forms.SubusuarioForm(request.POST, instance=subusuario)
        if form.is_valid():
            subusuario = form.save(commit=False)
            subusuario.rol = 'subusuario'
            subusuario.cliente = request.user
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                subusuario.set_password(form.cleaned_data['password'])
            subusuario.save()
            messages.success(request, "Subusuario actualizado.")
            return redirect('listado_subusuarios')
    else:
        form = forms.SubusuarioForm(instance=subusuario)

    return render(request, 'base/forms/editar_subusuario.html', {'form': form})

@login_required
def eliminar_subusuario(request, subusuario_id):
    if not request.user.es_cliente():
        return redirect('inicio')

    subusuario = get_object_or_404(request.user.empleados, id=subusuario_id)

    if request.method == 'POST':
        subusuario.delete()
        messages.success(request, "Subusuario eliminado.")
        return redirect('listado_subusuarios')

    return render(request, 'base/forms/confirmar_eliminar_subusuario.html', {'subusuario': subusuario})

