# `save_pessoa`

Arquivo: `clientes/facade.py`

Valida e grava o cadastro enviado pelo modal.

## Fluxo de Execução

1. Monta o `CadastraPessoa` com o POST (e a pessoa, na alteração).
2. Se inválido, devolve `html_form` com os erros para o modal.
3. Se válido, grava e escolhe a mensagem `clca0001` (adicionado) ou `clca0002` (alterado).
4. Troca o filtro para a função da pessoa salva (a não ser que seja `TODOS`), limpa a busca e devolve a lista com a pessoa selecionada no card de detalhes.

## Parâmetros

- `request` (`HttpRequest`): POST com os campos do form, `id_pessoa` (alteração) e `filtro`.

## Retorno

- `JsonResponse`: `html_form` (inválido) ou a resposta de `create_data_pessoas` com `mensagem` e `tipo`.

## Dependências

- [`CadastraPessoa`](../forms/CadastraPessoa.md).
- [`modal_pessoa`](modal_pessoa.md), [`create_data_pessoas`](create_data_pessoas.md).
- [`get_mensagem`](../../core/tools/get_mensagem.md).

## Código da Função

```{py3 linenums="1"}
def save_pessoa(request):
    id_pessoa = request.POST.get("id_pessoa")
    pessoa = get_pessoa_or_none(id_pessoa)
    form = CadastraPessoa(request.POST, instance=pessoa)

    if not form.is_valid():
        modal_html = modal_pessoa(request, id_pessoa, form)
        return JsonResponse({"html_form": modal_html})

    pessoa = form.save()
    codigo = "clca0002" if id_pessoa else "clca0001"
    mensagem = get_mensagem(
        codigo, funcao=pessoa.funcao, apelido=pessoa.apelido
    )
    # Mostra a lista onde a pessoa salva aparece, sem a busca anterior,
    # com ela selecionada no card de detalhes
    filtro = obter_filtro(request.POST.get("filtro"))
    if filtro != "TODOS":
        filtro = pessoa.funcao
    return create_data_pessoas(request, filtro, "", pessoa.pk, mensagem)
```

## Exemplo de Uso

```{py3 linenums="1"}
# POST /clientes/pessoa/form
return save_pessoa(request)
```
