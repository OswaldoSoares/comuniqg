# `get_usuario_or_none`

Arquivo: `account/facade.py`

Usuário do modal: `None` para novo, 404 se o id não existir.

## Fluxo de Execução

1. Sem id, `None`.
2. Com id, busca ou 404.

## Parâmetros

- `id_usuario`.

## Retorno

- `Account` ou `None`.

## Dependências

- `get_object_or_404`.

## Código da Função

```{py3 linenums="1"}
def get_usuario_or_none(id_usuario):
    if not id_usuario:
        return None
    return get_object_or_404(Account, pk=id_usuario)
```

## Exemplo de Uso

```{py3 linenums="1"}
get_usuario_or_none("")  # None
```
