# `modal_usuario`

Arquivo: `account/facade.py`

HTML do formulário do modal de novo ou alterar usuário.

## Fluxo de Execução

1. Busca o usuário (ou `None`).
2. Sem `form`, cria um com `_form_usuario`; com `form`, reaproveita os erros.
3. Renderiza `account/modal_usuario.html`.

## Parâmetros

- `request`, `id_usuario`, `form`.

## Retorno

- `str`: HTML.

## Dependências

- [`_form_usuario`](_form_usuario.md).

## Código da Função

```{py3 linenums="1"}
def modal_usuario(request, id_usuario=None, form=None):
    usuario = get_usuario_or_none(id_usuario)
    if form is None:
        form = _form_usuario(request, usuario)
    contexto = {"form": form, "usuario": usuario}
    return html_data.html_modal_usuario(request, contexto)
```

## Exemplo de Uso

```{py3 linenums="1"}
JsonResponse({"modal_html": modal_usuario(request, 3)})
```
