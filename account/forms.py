from typing import ClassVar

from django.contrib.auth import forms
from django.core.exceptions import ValidationError

from .models import Account


class AccountChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Account


class AccountCreationForm(forms.UserCreationForm):
    """Adicionar usuário no admin: e-mail (o login) e senha.

    O username, herdado do Django, recebe o próprio e-mail.
    """

    class Meta(forms.UserCreationForm.Meta):
        model = Account
        fields = ("email",)
        field_classes: ClassVar[dict] = {}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Account.objects.filter(email__iexact=email).exists():
            raise ValidationError("Já existe um usuário com este e-mail.")
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = usuario.email
        if commit:
            usuario.save()
        return usuario


class LoginForm(forms.AuthenticationForm):
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
