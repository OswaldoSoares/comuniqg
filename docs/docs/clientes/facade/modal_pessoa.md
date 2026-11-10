# `modal_pessoa`

Arquivo: `clientes/facade.py`

Gera o HTML do formulário do modal de cadastro ou alteração.

## Fluxo de Execução

1. Busca a pessoa (ou `None` para cadastro novo).
2. Sem `form`, cria um `CadastraPessoa` com a pessoa; com `form` (POST inválido), reaproveita-o com os erros.
3. Renderiza `clientes/modal_pessoa.html`.

## Parâmetros

- `request` (`HttpRequest`).
- `id_pessoa` (`int` ou `None`).
- `form` (`CadastraPessoa` ou `None`).

## Retorno

- `str`: HTML do formulário.

## Dependências

- [`get_pessoa_or_none`](get_pessoa_or_none.md).
- [`CadastraPessoa`](../forms/CadastraPessoa.md).
- `html_data.html_modal_pessoa`.

## Código da Função

```{py3 linenums="1"}
def modal_pessoa(request, id_pessoa=None, form=None):
    pessoa = get_pessoa_or_none(id_pessoa)
    if form is None:
        form = CadastraPessoa(instance=pessoa)
    contexto = {"form": form, "pessoa": pessoa}
    return html_data.html_modal_pessoa(request, contexto)
```

## Exemplo de Uso

```{py3 linenums="1"}
JsonResponse({"modal_html": modal_pessoa(request, 15)})
```
