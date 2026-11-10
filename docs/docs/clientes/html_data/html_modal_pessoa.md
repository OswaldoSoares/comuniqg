# `html_modal_pessoa`

Arquivo: `clientes/html_data.py`

Renderiza o formulário do modal (`clientes/modal_pessoa.html`).

## Fluxo de Execução

1. Renderiza o template com o contexto.

## Parâmetros

- `request`, `contexto` (`dict`): `form` e `pessoa`.

## Retorno

- `str`: HTML.

## Dependências

- `render_to_string`.

## Código da Função

```{py3 linenums="1"}
def html_modal_pessoa(request, contexto):
    return render_to_string(
        "clientes/modal_pessoa.html", contexto, request=request
    )
```

## Exemplo de Uso

```{py3 linenums="1"}
html = html_modal_pessoa(request, {"form": form, "pessoa": None})
```
