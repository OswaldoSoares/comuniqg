# `usuarios_lista`

Arquivo: `account/views.py`

Lista por ajax (filtro e busca).

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
def usuarios_lista(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_usuario = facade.obter_id(request.GET.get("id_usuario"))
    return facade.create_data_usuarios(
        request, filtro, request.GET.get("busca", ""), id_usuario
    )
```

## Exemplo de Uso

```{py3 linenums="1"}
# usuarios_lista(request)
```
