# `usuario_senha`

Arquivo: `account/views.py`

GET abre o modal de nova senha; POST salva.

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
@require_http_methods(["GET", "POST"])
def usuario_senha(request):
    """GET abre o modal de nova senha; POST salva."""
    if request.method == "POST":
        return facade.save_senha(request)
    id_usuario = facade.obter_id(request.GET.get("id_usuario"))
    modal_html = facade.modal_senha(request, id_usuario)
    return JsonResponse({"modal_html": modal_html})
```

## Exemplo de Uso

```{py3 linenums="1"}
# usuario_senha(request)
```
