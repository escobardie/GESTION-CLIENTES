## con esto Ahora {{ usuario_logeado }}
# está disponible en todas las plantillas, 
# sin necesidad de agregarlo manualmente en cada vista.

def datos_usuario(request):
    if request.user.is_authenticated:
        username = request.user.username
        is_empleado = request.user.usuario_padre 
        nombre = request.user.get_full_name() or request.user.username
        rol = getattr(request.user, 'rol', 'superusuario')  # fallback en caso de ser superuser
        if rol == "usuario":
            empresa = request.user.empresa_nombre
        else:
            empresa = request.user.usuario_padre.empresa_nombre
        
        return {
            'is_empleado': is_empleado,
            'username': username,
            'usuario_logeado': nombre,
            'usuario_rol': rol,
            'name_empresa' : empresa,
        }
    return {}
