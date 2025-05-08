# en tu archivo mixins.py (o donde prefieras)

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from apps.cliente.models import Cliente 

class ClienteAutorizacionMixin:
    def dispatch(self, request, *args, **kwargs):
        self.cliente_obj = get_object_or_404(Cliente, id=self.kwargs['id'])
        usuario_actual = (
            request.user.cliente
            if request.user.rol == 'subusuario'
            else request.user
        )
        if self.cliente_obj.usuario != usuario_actual:
            return redirect('acceso_denegado')  # o HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


