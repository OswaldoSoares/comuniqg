# `create_data_pessoa`

Arquivo: `clientes/facade.py`

Resposta JSON só com o card de detalhes, usada ao clicar numa linha da lista.

## Fluxo de Execução

1. Monta o contexto da pessoa (404 se não existir).
2. Renderiza `html-card-pessoa`.

## Parâmetros

- `request` (`HttpRequest`).
- `id_pessoa` (`int`).

## Retorno

- `JsonResponse`: `{"html-card-pessoa": ...}`.

## Dependências

- [`create_contexto_pessoa`](create_contexto_pessoa.md).
- `html_data.html_card_pessoa`.

## Código da Função

```{py3 linenums="1"}
def create_data_pessoa(request, id_pessoa):
    data = html_data.html_card_pessoa(
        request, create_contexto_pessoa(id_pessoa), {}
    )
    return JsonResponse(data)
```

## Exemplo de Uso

```{py3 linenums="1"}
return create_data_pessoa(request, 15)
```
