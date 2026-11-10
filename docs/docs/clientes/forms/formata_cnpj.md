# `formata_cnpj`

Arquivo: `clientes/forms.py`

Põe a máscara `00.000.000/0000-00`, como o Delphi grava.

## Fluxo de Execução

1. Fatia os 14 dígitos e junta com a pontuação.

## Parâmetros

- `d` (`str`): 14 dígitos.

## Retorno

- `str`.

## Dependências

- Nenhuma.

## Código da Função

```{py3 linenums="1"}
def formata_cnpj(d):
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"
```

## Exemplo de Uso

```{py3 linenums="1"}
formata_cnpj("11222333000181")  # "11.222.333/0001-81"
```
