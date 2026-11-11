# `html_modal_usuario`

Arquivo: `account/html_data.py`

Renderiza `account/modal_usuario.html`.

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
def html_modal_usuario(request, contexto):
    return render_to_string(
        "account/modal_usuario.html", contexto, request=request
    )
```

## Exemplo de Uso

```{py3 linenums="1"}
html_modal_usuario(request, contexto)
```
