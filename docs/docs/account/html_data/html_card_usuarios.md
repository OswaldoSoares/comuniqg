# `html_card_usuarios`

Arquivo: `account/html_data.py`

Renderiza `account/components/usuarios.html` na chave `html-card-usuarios`.

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
def html_card_usuarios(request, contexto, data):
    data["html-card-usuarios"] = render_to_string(
        "account/components/usuarios.html", contexto, request=request
    )
    return data
```

## Exemplo de Uso

```{py3 linenums="1"}
html_card_usuarios(request, contexto, {})
```
