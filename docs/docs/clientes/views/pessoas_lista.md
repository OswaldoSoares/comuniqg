# `pessoas_lista`

Arquivo: `clientes/views.py`

Lista por ajax, chamada ao trocar o filtro ou digitar na busca.

## Fluxo de Execução

1. Exige login.
2. Lê `filtro`, `busca` e `id_pessoa` (vazio ao trocar o filtro).
3. Devolve lista e card de detalhes.

## Parâmetros

- `request` (`HttpRequest`).

## Retorno

- `JsonResponse`: ver [`create_data_pessoas`](../facade/create_data_pessoas.md).

## Dependências

- `login_required`, `require_GET`.
- [`create_data_pessoas`](../facade/create_data_pessoas.md).

## Código da Função

```{py3 linenums="1"}
@login_required
@require_GET
def pessoas_lista(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_pessoa = facade.obter_id(request.GET.get("id_pessoa"))
    return facade.create_data_pessoas(
        request, filtro, request.GET.get("busca", ""), id_pessoa
    )
```

## Exemplo de Uso

```{py3 linenums="1"}
# GET /clientes/pessoas?filtro=FORNECEDOR&busca=&id_pessoa=
```
