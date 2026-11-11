from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def administrador_required(view):
    """Só superusuários (administradores). Sem login vai para o login;
    logado sem ser administrador recebe 403."""

    @login_required
    @wraps(view)
    def _view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return _view
