# `_form_usuario`

Arquivo: `account/facade.py`

Escolhe o formulário: novo usuário (com senha) ou alteração.

## Fluxo de Execução

1. Sem usuário, `NovoUsuarioForm`.
2. Com usuário, `UsuarioForm` com `editor=request.user`.

## Parâmetros

- `request`, `usuario` (`Account` ou `None`), `dados` (`QueryDict` ou `None`).

## Retorno

- Form.

## Dependências

- [`NovoUsuarioForm`](../forms/NovoUsuarioForm.md), [`UsuarioForm`](../forms/UsuarioForm.md).

## Código da Função

```{py3 linenums="1"}
def _form_usuario(request, usuario, dados=None):
    """Novo usuário (com senha) ou alteração (sem senha)."""
    if usuario is None:
        return NovoUsuarioForm(dados)
    return UsuarioForm(dados, instance=usuario, editor=request.user)
```

## Exemplo de Uso

```{py3 linenums="1"}
form = _form_usuario(request, None, request.POST)
```
