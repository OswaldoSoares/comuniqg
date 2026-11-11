# `index_usuarios`

Arquivo: `account/views.py`

Página da tela de usuários; aceita `filtro`, `busca` e `id_usuario` na URL.

## Fluxo de Execução

1. Exige administrador ([`administrador_required`](../decorators/administrador_required.md)).
2. Chama a função do facade correspondente.

## Parâmetros

- `request` (`HttpRequest`).

## Retorno

- `HttpResponse` ou `JsonResponse`.

## Dependências

- `account/facade.py`.

## Código da Função

```{py3 linenums="1"}
@administrador_required
@require_GET
def index_usuarios(request):
    """Lista de usuários e detalhes do selecionado (só administradores)."""
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_usuario = facade.obter_id(request.GET.get("id_usuario"))
    contexto = facade.create_contexto_usuarios(
        filtro, request.GET.get("busca"), id_usuario
    )
    if id_usuario:
        contexto.update(facade.create_contexto_usuario(request, id_usuario))
    return render(request, "account/usuarios.html", contexto)
```

## Exemplo de Uso

```{py3 linenums="1"}
# index_usuarios(request)
```
