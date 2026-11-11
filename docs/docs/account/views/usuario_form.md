# `usuario_form`

Arquivo: `account/views.py`

GET abre o modal de novo ou alterar; POST salva.

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
def usuario_form(request):
    """GET abre o modal de novo/alterar; POST salva."""
    if request.method == "POST":
        return facade.save_usuario(request)
    modal_html = facade.modal_usuario(request, request.GET.get("id_usuario"))
    return JsonResponse({"modal_html": modal_html})
```

## Exemplo de Uso

```{py3 linenums="1"}
# usuario_form(request)
```
