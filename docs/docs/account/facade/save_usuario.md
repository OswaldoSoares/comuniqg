# `save_usuario`

Arquivo: `account/facade.py`

Valida e grava o usuário enviado pelo modal.

## Fluxo de Execução

1. Monta o formulário com o POST.
2. Inválido: devolve `html_form` com os erros.
3. Válido: grava e responde com `acus0001` (novo) ou `acus0002` (alterado).

## Parâmetros

- `request`: POST com os campos, `id_usuario` (alteração) e `filtro`.

## Retorno

- `JsonResponse`.

## Dependências

- [`_form_usuario`](_form_usuario.md), [`modal_usuario`](modal_usuario.md), [`_resposta_lista`](_resposta_lista.md).

## Código da Função

```{py3 linenums="1"}
def save_usuario(request):
    id_usuario = request.POST.get("id_usuario")
    usuario = get_usuario_or_none(id_usuario)
    form = _form_usuario(request, usuario, request.POST)

    if not form.is_valid():
        modal_html = modal_usuario(request, id_usuario, form)
        return JsonResponse({"html_form": modal_html})

    usuario = form.save()
    codigo = "acus0002" if id_usuario else "acus0001"
    mensagem = get_mensagem(codigo, email=usuario.email)
    return _resposta_lista(request, usuario, mensagem)
```

## Exemplo de Uso

```{py3 linenums="1"}
return save_usuario(request)
```
