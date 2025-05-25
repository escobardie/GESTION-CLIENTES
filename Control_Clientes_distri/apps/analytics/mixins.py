from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from apps.cliente.models import Cliente 

class ClienteOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        print("Soy:")
        print(self.request.user)
        print("Mi jefe:")
        print(self.request.user.usuario_padre)
        print("mi rol:")
        print(self.request.user.rol)
        
        ## SOLO TENDRA ACCESO SI ESTA LOGUEADO Y SI ES CLIENTE (DUEÑO)
        return self.request.user.is_authenticated and self.request.user.es_usuario
    
    def handle_no_permission(self):
        return  redirect('acceso_denegado')

