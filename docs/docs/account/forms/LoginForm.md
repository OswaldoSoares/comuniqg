# `LoginForm`

Arquivo: `account/forms.py`

Formulário de login por e-mail (o `Account` usa `USERNAME_FIELD = "email"`). Usado pela `LoginView` em `account/urls.py`.

## Fluxo de Execução

1. Troca as mensagens de erro para português.
2. Renomeia os campos para E-MAIL e SENHA e põe `form-control`.

## Parâmetros

- Os mesmos do `AuthenticationForm`.

## Retorno

- Form do Django.

## Dependências

- `django.contrib.auth.forms.AuthenticationForm`.

## Código da Função

```{py3 linenums="1"}
class LoginForm(auth_forms.AuthenticationForm):
    """Formulário de login por e-mail (USERNAME_FIELD do Account)."""

    error_messages: ClassVar[dict] = {
        "invalid_login": "E-MAIL OU SENHA INVÁLIDOS.",
        "inactive": "USUÁRIO INATIVO.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "E-MAIL"
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "E-MAIL"}
        )
        self.fields["password"].label = "SENHA"
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "SENHA"}
        )
```

## Exemplo de Uso

```{py3 linenums="1"}
# account/urls.py
auth_views.LoginView.as_view(
    template_name="account/login.html", authentication_form=LoginForm
)
```
