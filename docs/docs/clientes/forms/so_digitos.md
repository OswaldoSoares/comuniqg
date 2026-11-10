# `so_digitos`

Arquivo: `clientes/forms.py`

Remove tudo o que não for dígito.

## Fluxo de Execução

1. Troca todo caractere não numérico por `""`.

## Parâmetros

- `valor` (`str` ou `None`).

## Retorno

- `str`.

## Dependências

- `re.sub`.

## Código da Função

```{py3 linenums="1"}
def so_digitos(valor):
    return re.sub(r"\D", "", valor or "")
```

## Exemplo de Uso

```{py3 linenums="1"}
so_digitos("11.222.333/0001-81")  # "11222333000181"
```
