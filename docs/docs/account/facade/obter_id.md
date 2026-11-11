# `obter_id`

Arquivo: `account/facade.py`

Converte o id recebido da tela em inteiro, ou `None`.

## Fluxo de Execução

1. Tenta `int(valor)`.
2. Valor vazio ou inválido vira `None`.

## Parâmetros

- `valor` (`str`, `int` ou `None`).

## Retorno

- `int` ou `None`.

## Dependências

- `int`.

## Código da Função

```{py3 linenums="1"}
def obter_id(valor):
    """Id numérico vindo da tela, ou None."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None
```

## Exemplo de Uso

```{py3 linenums="1"}
obter_id("3")  # 3
```
