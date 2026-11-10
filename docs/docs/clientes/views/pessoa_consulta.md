# `pessoa_consulta`

Arquivo: `clientes/views.py`

Card de detalhes de uma pessoa, chamado ao clicar numa linha da lista.

## Fluxo de Execução

1. Exige login.
2. Devolve o card; 404 se a pessoa não existir.

## Parâmetros

- `request` (`HttpRequest`): GET com `id_pessoa`.

## Retorno

- `JsonResponse`: `html-card-pessoa`.

## Dependências

- `login_required`, `require_GET`.
- [`create_data_pessoa`](../facade/create_data_pessoa.md).

## Código da Função

```{py3 linenums="1"}
@login_required
@require_GET
def pessoa_consulta(request):
    return facade.create_data_pessoa(
        request, facade.obter_id(request.GET.get("id_pessoa"))
    )
```

## Exemplo de Uso

```{py3 linenums="1"}
# GET /clientes/pessoa?id_pessoa=15
```
