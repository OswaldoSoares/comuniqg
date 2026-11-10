from django.contrib.auth import forms

from .models import Account


class AccountChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Account


class AccountCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Account


class LoginForm(forms.AuthenticationForm):
    """Formulário de login por e-mail (USERNAME_FIELD do Account)."""

    error_messages = {
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
