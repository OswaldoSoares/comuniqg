# `cnpj_valido`

Arquivo: `clientes/forms.py`

Confere os dois dígitos verificadores do CNPJ.

## Fluxo de Execução

1. Recusa se não tiver 14 dígitos ou se todos forem iguais.
2. Calcula os dois dígitos e compara com os informados.

## Parâmetros

- `digitos` (`str`): Só os dígitos.

## Retorno

- `bool`.

## Dependências

- [`_digito_verificador`](_digito_verificador.md).

## Código da Função

```{py3 linenums="1"}
def cnpj_valido(digitos):
    if len(digitos) != 14 or len(set(digitos)) == 1:
        return False
    numeros = [int(d) for d in digitos]
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    primeiro = _digito_verificador(numeros[:12], pesos)
    segundo = _digito_verificador(numeros[:13], [6, *pesos])
    return numeros[12] == primeiro and numeros[13] == segundo
```

## Exemplo de Uso

```{py3 linenums="1"}
cnpj_valido("11222333000181")  # True
```
