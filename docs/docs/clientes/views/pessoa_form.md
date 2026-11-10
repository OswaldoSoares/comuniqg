# `pessoa_form`

Arquivo: `clientes/views.py`

Abre o modal de cadastro ou alteração (GET) ou salva (POST).

## Fluxo de Execução

1. Exige login; aceita só GET e POST.
2. POST: chama `save_pessoa`.
3. GET: devolve o formulário em `modal_html`.

## Parâmetros

- `request` (`HttpRequest`): `id_pessoa` opcional (alteração).

## Retorno

- `JsonResponse`: `modal_html` (GET) ou a resposta de `save_pessoa` (POST).

## Dependências

- `login_required`, `require_http_methods`.
- [`save_pessoa`](../facade/save_pessoa.md), [`modal_pessoa`](../facade/modal_pessoa.md).

## Código da Função

```{py3 linenums="1"}
@login_required
@require_http_methods(["GET", "POST"])
def pessoa_form(request):
    if request.method == "POST":
        return facade.save_pessoa(request)

    modal_html = facade.modal_pessoa(request, request.GET.get("id_pessoa"))
    return JsonResponse({"modal_html": modal_html})
```

## Exemplo de Uso

```{py3 linenums="1"}
# GET /clientes/pessoa/form?id_pessoa=15 -> modal de alteração
```
