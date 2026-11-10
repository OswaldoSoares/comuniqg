# `cpf_valido`

Arquivo: `clientes/forms.py`

Confere os dois dígitos verificadores do CPF.

## Fluxo de Execução

1. Recusa se não tiver 11 dígitos ou se todos forem iguais.
2. Calcula os dois dígitos e compara com os informados.

## Parâmetros

- `digitos` (`str`): Só os dígitos.

## Retorno

- `bool`.

## Dependências

- [`_digito_verificador`](_digito_verificador.md).

## Código da Função

```{py3 linenums="1"}
def cpf_valido(digitos):
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    numeros = [int(d) for d in digitos]
    primeiro = _digito_verificador(numeros[:9], range(10, 1, -1))
    segundo = _digito_verificador(numeros[:10], range(11, 1, -1))
    return numeros[9] == primeiro and numeros[10] == segundo
```

## Exemplo de Uso

```{py3 linenums="1"}
cpf_valido("52998224725")  # True
```
