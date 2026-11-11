# `NovoUsuarioForm`

Arquivo: `account/forms.py`

Novo usuário na tela de usuários: os campos do [`UsuarioForm`](UsuarioForm.md) mais a senha duas vezes.

## Fluxo de Execução

1. Valida os campos do `UsuarioForm`.
2. Confere se as senhas são iguais e passa a senha pelos validadores do Django (tamanho, só números, senha comum, parecida com nome ou e-mail).
3. `save` grava a senha criptografada.

## Parâmetros

- `data` (`QueryDict`): campos do usuário, `senha1` e `senha2`.

## Retorno

- `save()` retorna o `Account`.

## Dependências

- `_SenhaDupla` (campos e conferência da senha).
- `django.contrib.auth.password_validation`.

## Código da Função

```{py3 linenums="1"}
class NovoUsuarioForm(_SenhaDupla, UsuarioForm):
    """Novo usuário: os campos da alteração mais a senha."""

    def clean(self):
        dados = super().clean()
        usuario = Account(
            email=dados.get("email") or "",
            first_name=dados.get("first_name") or "",
            last_name=dados.get("last_name") or "",
        )
        self._confere_senha(usuario)
        return dados

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["senha1"])
        if commit:
            usuario.save()
        return usuario
```

## Exemplo de Uso

```{py3 linenums="1"}
form = NovoUsuarioForm(request.POST)
if form.is_valid():
    usuario = form.save()
```
