# `modal_senha`

Arquivo: `account/facade.py`

HTML do modal de nova senha.

## Fluxo de Execução

1. Busca o usuário (404 se não existir).
2. Renderiza `account/modal_senha.html`.

## Parâmetros

- `request`, `id_usuario`, `form`.

## Retorno

- `str`: HTML.

## Dependências

- [`SenhaUsuarioForm`](../forms/SenhaUsuarioForm.md).

## Código da Função

```{py3 linenums="1"}
def modal_senha(request, id_usuario, form=None):
    usuario = get_object_or_404(Account, pk=id_usuario)
    if form is None:
        form = SenhaUsuarioForm(usuario)
    contexto = {"form": form, "usuario": usuario}
    return html_data.html_modal_senha(request, contexto)
```

## Exemplo de Uso

```{py3 linenums="1"}
JsonResponse({"modal_html": modal_senha(request, 3)})
```
