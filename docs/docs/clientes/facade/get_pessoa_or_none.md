# `get_pessoa_or_none`

Arquivo: `clientes/facade.py`

Busca a pessoa do modal: `None` para cadastro novo, 404 se o id não existir.

## Fluxo de Execução

1. Sem id, retorna `None`.
2. Com id, busca a pessoa ou gera 404.

## Parâmetros

- `id_pessoa` (`str`, `int` ou `None`).

## Retorno

- `Pessoa` ou `None`.

## Dependências

- `get_object_or_404(...)`.

## Código da Função

```{py3 linenums="1"}
def get_pessoa_or_none(id_pessoa):
    if not id_pessoa:
        return None
    return get_object_or_404(Pessoa, pk=id_pessoa)
```

## Exemplo de Uso

```{py3 linenums="1"}
get_pessoa_or_none("")  # None (cadastro novo)
```
