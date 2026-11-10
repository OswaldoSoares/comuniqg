# `_digito_verificador`

Arquivo: `clientes/forms.py`

Calcula um dígito verificador pelo módulo 11 (usado no CNPJ e no CPF).

## Fluxo de Execução

1. Soma os números multiplicados pelos pesos e tira o resto por 11.
2. Resto menor que 2 dá 0; senão, 11 menos o resto.

## Parâmetros

- `numeros` (`list[int]`).
- `pesos` (iterável de `int`).

## Retorno

- `int`: Dígito de 0 a 9.

## Dependências

- Nenhuma.

## Código da Função

```{py3 linenums="1"}
def _digito_verificador(numeros, pesos):
    resto = sum(n * p for n, p in zip(numeros, pesos)) % 11
    return 0 if resto < 2 else 11 - resto
```

## Exemplo de Uso

```{py3 linenums="1"}
_digito_verificador([5, 2, 9, 9, 8, 2, 2, 4, 7], range(10, 1, -1))  # 2
```
