# `html_card_usuario`

Arquivo: `account/html_data.py`

Renderiza `account/components/usuario.html` na chave `html-card-usuario`.

## Fluxo de Execução

1. Renderiza o template com o contexto.

## Parâmetros

- `request`, `contexto` (`dict`) e, nos cards, `data` (`dict`).

## Retorno

- `dict` (cards) ou `str` (modais).

## Dependências

- `render_to_string`.

## Código da Função

```{py3 linenums="1"}
def html_card_usuario(request, contexto, data):
    data["html-card-usuario"] = render_to_string(
        "account/components/usuario.html", contexto, request=request
    )
    return data
```

## Exemplo de Uso

```{py3 linenums="1"}
html_card_usuario(request, contexto, {})
```
