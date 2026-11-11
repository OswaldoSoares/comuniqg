# `create_data_usuarios`

Arquivo: `account/facade.py`

Resposta JSON com a lista e o card do usuário selecionado. Sem seleção, o card volta para "Selecione um usuário na lista...".

## Fluxo de Execução

1. Renderiza `html-card-usuarios` e `html-card-usuario`.
2. Inclui `filtro`, `busca` e `id_usuario`.
3. Inclui `mensagem` e `tipo` quando houver.

## Parâmetros

- `request`, `filtro`, `busca`, `id_usuario`, `mensagem` (`dict` ou `None`).

## Retorno

- `JsonResponse`.

## Dependências

- [`create_contexto_usuarios`](create_contexto_usuarios.md), [`create_contexto_usuario`](create_contexto_usuario.md).

## Código da Função

```{py3 linenums="1"}
def create_data_usuarios(
    request, filtro, busca="", id_usuario=None, mensagem=None
):
    """Resposta JSON com a lista e o card do usuário selecionado.

    Sem usuário selecionado, o card de detalhes volta vazio.
    """
    contexto = create_contexto_usuarios(filtro, busca, id_usuario)
    data = html_data.html_card_usuarios(request, contexto, {})
    contexto_usuario = (
        create_contexto_usuario(request, id_usuario) if id_usuario else {}
    )
    data = html_data.html_card_usuario(request, contexto_usuario, data)
    data.update(
        {"filtro": filtro, "busca": busca, "id_usuario": id_usuario or ""}
    )
    if mensagem:
        data.update(mensagem)
    return JsonResponse(data)
```

## Exemplo de Uso

```{py3 linenums="1"}
create_data_usuarios(request, "ATIVOS", "", None)
```
