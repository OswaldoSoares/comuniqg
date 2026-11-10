# `obter_id`

Arquivo: `clientes/facade.py`

Converte um identificador recebido da tela em inteiro, sem gerar erro quando o valor é inválido.

## Fluxo de Execução

1. Tenta converter `valor` com `int(...)`.
2. Retorna `None` se o valor for vazio, `None` ou não numérico.

## Parâmetros

- `valor` (`str`, `int` ou `None`): Identificador enviado por GET ou POST.

## Retorno

- `int` ou `None`.

## Dependências

- `int(...)`.

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
obter_id("15")  # 15
obter_id("")    # None
```
