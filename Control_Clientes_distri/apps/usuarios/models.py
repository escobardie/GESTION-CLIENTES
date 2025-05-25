from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('superusuario', 'Superusuario'),
        ('usuario', 'Usuario'),
        ('subusuario', 'Subusuario'),
    )

    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')
    usuario_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='empleados')
    telefono = models.CharField(max_length=20, null=True, blank=True)
    empresa_nombre = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"

    @property
    def es_superusuario(self):
        return self.rol == 'superusuario'

    @property
    def es_usuario(self):
        return self.rol == 'usuario'

    @property
    def es_subusuario(self):
        return self.rol == 'subusuario'

    def clean(self):
        if self.rol == 'subusuario' and not self.usuario_padre:
            raise ValidationError("Un subusuario debe tener un usuario padre asociado.")
        if self.rol in ['usuario', 'superusuario'] and self.usuario_padre:
            raise ValidationError(f"Un usuario con rol '{self.rol}' no debe tener un usuario padre.")
