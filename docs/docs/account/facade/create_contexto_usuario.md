# `create_contexto_usuario`

Arquivo: `account/facade.py`

Contexto do card de detalhes do usuário.

## Fluxo de Execução

1. Busca o usuário; 404 se não existir.
2. Marca `eu` quando é o usuário logado (o card esconde o inativar).

## Parâmetros

- `request` (`HttpRequest`).
- `id_usuario` (`int`).

## Retorno

- `dict`: `usuario`, `eu`.

## Dependências

- `get_object_or_404`.

## Código da Função

```{py3 linenums="1"}
def create_contexto_usuario(request, id_usuario):
    """Usuário selecionado para o card de detalhes."""
    usuario = get_object_or_404(Account, pk=id_usuario)
    return {"usuario": usuario, "eu": usuario.pk == request.user.pk}
```

## Exemplo de Uso

```{py3 linenums="1"}
create_contexto_usuario(request, 3)
```
