# `save_senha`

Arquivo: `account/facade.py`

Grava a nova senha definida pelo administrador.

## Fluxo de Execução

1. Valida o `SenhaUsuarioForm`; inválido devolve `html_form`.
2. Grava a senha.
3. Se for a senha do próprio administrador, renova a sessão (`update_session_auth_hash`) para ele continuar logado.
4. Responde com `acus0003`.

## Parâmetros

- `request`: POST com `id_usuario`, `senha1`, `senha2`.

## Retorno

- `JsonResponse`.

## Dependências

- [`SenhaUsuarioForm`](../forms/SenhaUsuarioForm.md), [`_resposta_lista`](_resposta_lista.md).

## Código da Função

```{py3 linenums="1"}
def save_senha(request):
    """Nova senha definida pelo administrador."""
    usuario = get_object_or_404(Account, pk=request.POST.get("id_usuario"))
    form = SenhaUsuarioForm(usuario, request.POST)
    if not form.is_valid():
        modal_html = modal_senha(request, usuario.pk, form)
        return JsonResponse({"html_form": modal_html})

    form.save()
    if usuario.pk == request.user.pk:
        # Trocar a própria senha encerraria a sessão
        update_session_auth_hash(request, usuario)
    mensagem = get_mensagem("acus0003", email=usuario.email)
    return _resposta_lista(request, usuario, mensagem)
```

## Exemplo de Uso

```{py3 linenums="1"}
return save_senha(request)
```
