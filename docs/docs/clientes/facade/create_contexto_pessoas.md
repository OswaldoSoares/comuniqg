# `create_contexto_pessoas`

Arquivo: `clientes/facade.py`

Monta o contexto da lista de pessoas (card principal).

## Fluxo de Execução

1. Busca as pessoas com `get_pessoas`.
2. Devolve a lista, os filtros, o filtro e a busca usados, o total e a pessoa selecionada.

## Parâmetros

- `filtro` (`str`): Filtro de função.
- `busca` (`str`): Texto da busca.
- `id_pessoa` (`int` ou `None`): Pessoa selecionada (linha destacada).

## Retorno

- `dict`: `pessoas`, `filtros`, `filtro`, `busca`, `total`, `id_pessoa`.

## Dependências

- [`get_pessoas`](get_pessoas.md).

## Código da Função

```{py3 linenums="1"}
def create_contexto_pessoas(filtro=FILTRO_PADRAO, busca="", id_pessoa=None):
    pessoas = list(get_pessoas(filtro, busca))
    return {
        "pessoas": pessoas,
        "filtros": FILTROS,
        "filtro": filtro,
        "busca": busca,
        "total": len(pessoas),
        "id_pessoa": id_pessoa,
    }
```

## Exemplo de Uso

```{py3 linenums="1"}
contexto = create_contexto_pessoas("FORNECEDOR", "", 15)
contexto["total"]
```
