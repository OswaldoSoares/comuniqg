# `create_contexto_usuarios`

Arquivo: `account/facade.py`

Contexto da lista de usuários.

## Fluxo de Execução

1. Busca os usuários.
2. Devolve a lista, os filtros, o filtro e a busca, o total e o selecionado.

## Parâmetros

- `filtro`, `busca`, `id_usuario` (`int` ou `None`).

## Retorno

- `dict`: `usuarios`, `filtros`, `filtro`, `busca`, `total`, `id_usuario`.

## Dependências

- [`get_usuarios`](get_usuarios.md).

## Código da Função

```{py3 linenums="1"}
def create_contexto_usuarios(filtro=FILTRO_PADRAO, busca="", id_usuario=None):
    usuarios = list(get_usuarios(filtro, busca))
    return {
        "usuarios": usuarios,
        "filtros": FILTROS,
        "filtro": filtro,
        "busca": busca,
        "total": len(usuarios),
        "id_usuario": id_usuario,
    }
```

## Exemplo de Uso

```{py3 linenums="1"}
create_contexto_usuarios("ATIVOS", "", 3)
```
