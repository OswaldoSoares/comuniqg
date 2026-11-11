# `AccountCreationForm`

Arquivo: `account/forms.py`

Formulário da tela "Adicionar usuário" do admin: e-mail e senha.

## Fluxo de Execução

1. Mostra só o e-mail e as duas senhas (`AccountAdmin.add_fieldsets`).
2. `clean_email` põe em minúsculas e recusa e-mail já cadastrado (sem diferenciar maiúsculas).
3. As senhas passam pelos validadores do Django (`UserCreationForm`).
4. `save` copia o e-mail para o `username`.

## Parâmetros

- `data` (`QueryDict`): `email`, `password1`, `password2`.

## Retorno

- `save()` retorna o `Account` gravado.

## Dependências

- `django.contrib.auth.forms.UserCreationForm`.
- `AccountAdmin` (`account/admin.py`).

## Código da Função

```{py3 linenums="1"}
class AccountCreationForm(auth_forms.UserCreationForm):
    """Adicionar usuário no admin: e-mail (o login) e senha.

    O username, herdado do Django, recebe o próprio e-mail.
    """

    class Meta(auth_forms.UserCreationForm.Meta):
        model = Account
        fields = ("email",)
        field_classes: ClassVar[dict] = {}

    def clean_email(self):
        return _email_livre(self.cleaned_data["email"])

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = usuario.email
        if commit:
            usuario.save()
        return usuario
```

## Exemplo de Uso

```{py3 linenums="1"}
form = AccountCreationForm({"email": "fulano@empresa.com.br",
                            "password1": "S3nha-forte",
                            "password2": "S3nha-forte"})
if form.is_valid():
    usuario = form.save()
```
