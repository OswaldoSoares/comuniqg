# `_resposta_lista`

Arquivo: `account/facade.py`

Resposta depois de salvar, trocar senha ou mudar a situação: a lista com o usuário selecionado e sem a busca anterior.

## Fluxo de Execução

1. Lê o filtro do POST.
2. Se o filtro esconderia o usuário (ex.: inativado com o filtro `ATIVOS`), passa para `TODOS`.
3. Devolve `create_data_usuarios` com a mensagem.

## Parâmetros

- `request`, `usuario` (`Account`), `mensagem` (`dict`).

## Retorno

- `JsonResponse`.

## Dependências

- [`create_data_usuarios`](create_data_usuarios.md).

## Código da Função

```{py3 linenums="1"}
def _resposta_lista(request, usuario, mensagem):
    """Lista com o usuário salvo selecionado, sem a busca anterior.

    Se o filtro atual esconderia o usuário, mostra todos.
    """
    filtro = obter_filtro(request.POST.get("filtro"))
    if (filtro == "ATIVOS" and not usuario.is_active) or (
        filtro == "INATIVOS" and usuario.is_active
    ):
        filtro = "TODOS"
    return create_data_usuarios(request, filtro, "", usuario.pk, mensagem)
```

## Exemplo de Uso

```{py3 linenums="1"}
return _resposta_lista(request, usuario, mensagem)
```
