from django.conf import settings

class DatabaseRouterMiddleware:
    """
    Middleware que selecciona la base de datos en función del usuario.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determina la base de datos a usar para la solicitud
        self._set_database_for_user(request)
        response = self.get_response(request)
        return response

    def _set_database_for_user(self, request):
        # Suponiendo que la base de datos se determina por el usuario autenticado
        if request.user.is_authenticated:
            user = request.user
            # Determina qué base de datos usar
            if user.profile.use_other_db:
                request._database = 'other_db'
            else:
                request._database = 'default'
        else:
            request._database = 'default'

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, '_database'):
            # Puedes usar este atributo para dirigir las consultas a la base de datos correcta
            pass
        return None

