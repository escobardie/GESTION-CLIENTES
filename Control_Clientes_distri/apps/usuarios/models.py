# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('superusuario', 'Superusuario'),
        ('cliente', 'Cliente'),
        ('subusuario', 'Subusuario'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    cliente = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='empleados')
    telefono = models.CharField(max_length=20, null=True, blank=True)
    empresa_nombre = models.CharField(max_length=255, null=True, blank=True)

    def es_superusuario(self):
        return self.rol == 'superusuario'
    
    def es_cliente(self):
        return self.rol == 'cliente'
    
    def es_subusuario(self):
        return self.rol == 'subusuario'
