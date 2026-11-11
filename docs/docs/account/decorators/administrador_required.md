# `administrador_required`

Arquivo: `account/decorators.py`

Decorator das views da tela de usuários: só superusuários entram.

## Fluxo de Execução

1. Sem login: `login_required` manda para o login (com `next`).
2. Logado sem ser superusuário: levanta `PermissionDenied` (403).
3. Superusuário: chama a view.

## Parâmetros

- `view` (função): View a proteger.

## Retorno

- Função: a view protegida.

## Dependências

- `login_required`, `PermissionDenied`.

## Código da Função

```{py3 linenums="1"}
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
```

## Exemplo de Uso

```{py3 linenums="1"}
@administrador_required
def index_usuarios(request):
    ...
```
