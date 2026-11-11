# `alterar_situacao_usuario`

Arquivo: `account/facade.py`

Ativa ou inativa o usuário. Inativo não consegue entrar no sistema.

## Fluxo de Execução

1. Busca o usuário.
2. Se for o próprio usuário logado, recusa com `acus0006`.
3. Inverte `is_active` e responde com `acus0004` (ativado) ou `acus0005` (inativado).

## Parâmetros

- `request`: POST com `id_usuario` e `filtro`.

## Retorno

- `JsonResponse`.

## Dependências

- [`_resposta_lista`](_resposta_lista.md).

## Código da Função

```{py3 linenums="1"}
def alterar_situacao_usuario(request):
    """Ativa ou inativa; ninguém inativa o próprio usuário."""
    usuario = get_object_or_404(Account, pk=request.POST.get("id_usuario"))
    if usuario.pk == request.user.pk:
        return _resposta_lista(request, usuario, get_mensagem("acus0006"))

    usuario.is_active = not usuario.is_active
    usuario.save(update_fields=["is_active"])
    codigo = "acus0004" if usuario.is_active else "acus0005"
    mensagem = get_mensagem(codigo, email=usuario.email)
    return _resposta_lista(request, usuario, mensagem)
```

## Exemplo de Uso

```{py3 linenums="1"}
return alterar_situacao_usuario(request)
```
