# `index_clientes`

Arquivo: `clientes/views.py`

Página do cadastro (`/clientes/`): lista à esquerda e card de detalhes à direita.

## Fluxo de Execução

1. Exige login.
2. Lê `filtro`, `busca` e `id_pessoa` da URL.
3. Monta a lista e, com `id_pessoa`, o card da pessoa.
4. Renderiza `clientes/index.html`.

## Parâmetros

- `request` (`HttpRequest`): GET com `filtro`, `busca` e `id_pessoa` opcionais.

## Retorno

- `HttpResponse`.

## Dependências

- `login_required`, `require_GET`.
- [`obter_filtro`](../facade/obter_filtro.md), [`obter_id`](../facade/obter_id.md), [`create_contexto_pessoas`](../facade/create_contexto_pessoas.md), [`create_contexto_pessoa`](../facade/create_contexto_pessoa.md).

## Código da Função

```{py3 linenums="1"}
@login_required
@require_GET
def index_clientes(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_pessoa = facade.obter_id(request.GET.get("id_pessoa"))
    contexto = facade.create_contexto_pessoas(
        filtro, request.GET.get("busca"), id_pessoa
    )
    if id_pessoa:
        contexto.update(facade.create_contexto_pessoa(id_pessoa))
    return render(request, "clientes/index.html", contexto)
```

## Exemplo de Uso

```{py3 linenums="1"}
# GET /clientes/?id_pessoa=15 -> abre com a pessoa 15 selecionada
```
