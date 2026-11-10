# `_sem_pontuacao`

Arquivo: `clientes/facade.py`

Monta uma expressão SQL que remove `.`, `/` e `-` de uma coluna, para buscar CNPJ e CPF digitados com ou sem máscara.

## Fluxo de Execução

1. Começa com o nome da coluna.
2. Envolve a expressão em um `Replace` para cada caractere de pontuação.

## Parâmetros

- `campo` (`str`): Nome do campo do model (`"cnpj"` ou `"cpf"`).

## Retorno

- `Replace`: Expressão para usar em `annotate`.

## Dependências

- `django.db.models.functions.Replace`, `Value`.

## Código da Função

```{py3 linenums="1"}
def _sem_pontuacao(campo):
    """Documento só com dígitos, para buscar com ou sem máscara."""
    expressao = campo
    for caractere in "./-":
        expressao = Replace(expressao, Value(caractere), Value(""))
    return expressao
```

## Exemplo de Uso

```{py3 linenums="1"}
Pessoa.objects.annotate(cnpj_digitos=_sem_pontuacao("cnpj"))
```
