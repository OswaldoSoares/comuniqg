# `create_data_pessoas`

Arquivo: `clientes/facade.py`

Resposta JSON com a lista e o card da pessoa selecionada. Sem pessoa selecionada, o card de detalhes volta vazio ("Selecione um cadastro na lista...").

## Fluxo de Execução

1. Monta o contexto da lista e renderiza `html-card-pessoas`.
2. Renderiza `html-card-pessoa` com a pessoa ou vazio.
3. Inclui `filtro`, `busca` e `id_pessoa` (`""` sem seleção).
4. Se houver `mensagem`, inclui `mensagem` e `tipo` para o toast.

## Parâmetros

- `request` (`HttpRequest`).
- `filtro` (`str`), `busca` (`str`).
- `id_pessoa` (`int` ou `None`).
- `mensagem` (`dict` ou `None`): Resultado de `get_mensagem`.

## Retorno

- `JsonResponse`.

## Dependências

- [`create_contexto_pessoas`](create_contexto_pessoas.md), [`create_contexto_pessoa`](create_contexto_pessoa.md).
- `html_data.html_card_pessoas`, `html_data.html_card_pessoa`.

## Código da Função

```{py3 linenums="1"}
def create_data_pessoas(
    request, filtro, busca="", id_pessoa=None, mensagem=None
):
    """Resposta JSON com a lista e o card da pessoa selecionada.

    Sem pessoa selecionada, o card de detalhes volta vazio.
    """
    contexto = create_contexto_pessoas(filtro, busca, id_pessoa)
    data = html_data.html_card_pessoas(request, contexto, {})
    contexto_pessoa = create_contexto_pessoa(id_pessoa) if id_pessoa else {}
    data = html_data.html_card_pessoa(request, contexto_pessoa, data)
    data.update(
        {"filtro": filtro, "busca": busca, "id_pessoa": id_pessoa or ""}
    )
    if mensagem:
        data.update(mensagem)
    return JsonResponse(data)
```

## Exemplo de Uso

```{py3 linenums="1"}
return create_data_pessoas(request, "CLIENTE", "", 15, mensagem)
```
