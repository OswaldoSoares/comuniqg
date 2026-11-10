# `obter_filtro`

Arquivo: `clientes/facade.py`

Normaliza o filtro de função recebido da tela (`CLIENTE`, `FORNECEDOR` ou `TODOS`), sem gerar erro quando o valor é inválido.

## Fluxo de Execução

1. Converte o valor para maiúsculas (vazio ou `None` vira `""`).
2. Retorna o valor se ele estiver em `FILTROS`; senão retorna `FILTRO_PADRAO` (`CLIENTE`).

## Parâmetros

- `valor` (`str` ou `None`): Filtro enviado por GET ou POST.

## Retorno

- `str`: `CLIENTE`, `FORNECEDOR` ou `TODOS`.

## Dependências

- `FILTROS`, `FILTRO_PADRAO`: Constantes do módulo.

## Código da Função

```{py3 linenums="1"}
def obter_filtro(valor):
    valor = (valor or "").upper()
    return valor if valor in dict(FILTROS) else FILTRO_PADRAO
```

## Exemplo de Uso

```{py3 linenums="1"}
obter_filtro("fornecedor")  # "FORNECEDOR"
obter_filtro("qualquer")    # "CLIENTE"
```
