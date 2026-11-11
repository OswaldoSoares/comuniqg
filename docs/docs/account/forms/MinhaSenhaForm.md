# `MinhaSenhaForm`

Arquivo: `account/forms.py`

O próprio usuário troca a senha em `/account/senha`.

## Fluxo de Execução

1. Usa o `PasswordChangeForm` do Django: confere a senha atual, as duas novas e os validadores.
2. Só troca rótulos e classes para o visual ui.

## Parâmetros

- `user` (`Account`), `data` (`QueryDict`): `old_password`, `new_password1`, `new_password2`.

## Retorno

- Form do Django.

## Dependências

- `django.contrib.auth.forms.PasswordChangeForm`.
- `PasswordChangeView` (`account/urls.py`), que mantém o login depois da troca.

## Código da Função

```{py3 linenums="1"}
class MinhaSenhaForm(auth_forms.PasswordChangeForm):
    """O próprio usuário troca a senha: atual e nova (duas vezes)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rotulos = {
            "old_password": "SENHA ATUAL",
            "new_password1": "NOVA SENHA",
            "new_password2": "CONFIRME A NOVA SENHA",
        }
        for nome, rotulo in rotulos.items():
            self.fields[nome].label = rotulo
            self.fields[nome].help_text = ""
            self.fields[nome].widget.attrs["class"] = "form-control"
```

## Exemplo de Uso

```{py3 linenums="1"}
# account/urls.py
auth_views.PasswordChangeView.as_view(
    template_name="account/minha_senha.html", form_class=MinhaSenhaForm
)
```
