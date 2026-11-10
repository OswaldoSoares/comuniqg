# `formata_cpf`

Arquivo: `clientes/forms.py`

Põe a máscara `000.000.000-00`, como o Delphi grava.

## Fluxo de Execução

1. Fatia os 11 dígitos e junta com a pontuação.

## Parâmetros

- `d` (`str`): 11 dígitos.

## Retorno

- `str`.

## Dependências

- Nenhuma.

## Código da Função

```{py3 linenums="1"}
def formata_cpf(d):
    return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"
```

## Exemplo de Uso

```{py3 linenums="1"}
formata_cpf("52998224725")  # "529.982.247-25"
```
