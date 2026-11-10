# `preenchido`

Arquivo: `clientes/forms.py`

Devolve o valor gravado pelo usuário ou `""` quando ele é a máscara zerada do Delphi (`000.000.000-00`, `00000-000`, `(00)00000-0000`...).

## Fluxo de Execução

1. Remove espaços das pontas (`None` vira `""`).
2. Se o valor só tiver zeros, pontos, hífens, barras, parênteses e espaços, devolve `""`.

## Parâmetros

- `valor` (`str` ou `None`).

## Retorno

- `str`.

## Dependências

- Nenhuma.

## Código da Função

```{py3 linenums="1"}
def preenchido(valor):
    """Valor gravado pelo usuário; a máscara zerada do Delphi vira ''."""
    valor = (valor or "").strip()
    return valor if valor.strip(" .-/()0") else ""
```

## Exemplo de Uso

```{py3 linenums="1"}
preenchido("000.000.000-00")  # ""
preenchido("ISENTO")          # "ISENTO"
```
