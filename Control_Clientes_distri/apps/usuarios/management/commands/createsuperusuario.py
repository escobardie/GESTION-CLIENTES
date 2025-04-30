from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuserCommand
from django.core.management import CommandError

class Command(CreateSuperuserCommand):
    help = 'Crea un superusuario y automáticamente asigna rol = superusuario.'

    def handle(self, *args, **options):
        options['rol'] = 'superusuario'  # Forzar el rol en las opciones
        super().handle(*args, **options)

    def save_user(self, user, **kwargs):
        User = get_user_model()
        if hasattr(user, 'rol'):
            user.rol = 'superusuario'
        user.save()
