# `obter_filtro`

Arquivo: `account/facade.py`

Normaliza o filtro de situação (`ATIVOS`, `INATIVOS` ou `TODOS`).

## Fluxo de Execução

1. Põe em maiúsculas.
2. Valor inválido vira `ATIVOS`.

## Parâmetros

- `valor` (`str` ou `None`).

## Retorno

- `str`.

## Dependências

- `FILTROS`.

## Código da Função

```{py3 linenums="1"}
def obter_filtro(valor):
    valor = (valor or "").upper()
    return valor if valor in dict(FILTROS) else FILTRO_PADRAO
```

## Exemplo de Uso

```{py3 linenums="1"}
obter_filtro("todos")  # "TODOS"
```
