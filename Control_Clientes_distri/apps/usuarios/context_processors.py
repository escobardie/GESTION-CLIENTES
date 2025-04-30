## con esto Ahora {{ usuario_logeado }}
# está disponible en todas las plantillas, 
# sin necesidad de agregarlo manualmente en cada vista.

def datos_usuario(request):
    if request.user.is_authenticated:
        username = request.user.username
        is_empleado = request.user.cliente
        nombre = request.user.get_full_name() or request.user.username
        rol = getattr(request.user, 'rol', 'superusuario')  # fallback en caso de ser superuser
        return {
            'is_empleado': is_empleado,
            'username': username,
            'usuario_logeado': nombre,
            'usuario_rol': rol,
        }
    return {}
