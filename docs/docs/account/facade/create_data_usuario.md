# `create_data_usuario`

Arquivo: `account/facade.py`

Resposta JSON só com o card de detalhes (clique na linha).

## Fluxo de Execução

1. Monta o contexto do usuário.
2. Renderiza `html-card-usuario`.

## Parâmetros

- `request`, `id_usuario` (`int`).

## Retorno

- `JsonResponse`.

## Dependências

- [`create_contexto_usuario`](create_contexto_usuario.md).

## Código da Função

```{py3 linenums="1"}
def create_data_usuario(request, id_usuario):
    data = html_data.html_card_usuario(
        request, create_contexto_usuario(request, id_usuario), {}
    )
    return JsonResponse(data)
```

## Exemplo de Uso

```{py3 linenums="1"}
create_data_usuario(request, 3)
```
