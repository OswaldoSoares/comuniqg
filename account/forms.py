from typing import ClassVar

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import Account


class AccountChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = Account


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


# --- Tela de usuários (account/usuarios) -------------------------------------

SIM_NAO = ((False, "NÃO"), (True, "SIM"))


def _email_livre(email, usuario=None):
    """E-mail em minúsculas, recusado se outro usuário já o usa."""
    email = email.strip().lower()
    repetido = Account.objects.filter(email__iexact=email)
    if usuario is not None and usuario.pk:
        repetido = repetido.exclude(pk=usuario.pk)
    if repetido.exists():
        raise ValidationError("Já existe um usuário com este e-mail.")
    return email


class _SenhaDupla(forms.Form):
    """Senha digitada duas vezes e conferida pelos validadores do Django."""

    senha1 = forms.CharField(
        label="SENHA",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )
    senha2 = forms.CharField(
        label="CONFIRME A SENHA",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )

    def _confere_senha(self, usuario):
        senha1 = self.cleaned_data.get("senha1")
        senha2 = self.cleaned_data.get("senha2")
        if senha1 and senha2 and senha1 != senha2:
            self.add_error("senha2", "As senhas não conferem.")
            return
        if senha1:
            try:
                password_validation.validate_password(senha1, usuario)
            except ValidationError as erro:
                self.add_error("senha1", erro)


class UsuarioForm(forms.ModelForm):
    """Alterar usuário: nome, e-mail e administrador.

    O próprio usuário não pode tirar o seu acesso de administrador
    (o campo fica desabilitado), para não ficar trancado fora da tela.
    """

    is_superuser = forms.BooleanField(
        label="ADMINISTRADOR",
        required=False,
        widget=forms.Select(choices=SIM_NAO),
    )

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email", "is_superuser")
        labels: ClassVar[dict] = {
            "first_name": "NOME",
            "last_name": "SOBRENOME",
            "email": "E-MAIL",
        }

    def __init__(self, *args, editor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        for campo in self.fields.values():
            campo.widget.attrs.setdefault("class", "form-control")
            campo.widget.attrs.setdefault("autocomplete", "off")
        if editor is not None and editor.pk == self.instance.pk:
            self.fields["is_superuser"].disabled = True
            self.fields[
                "is_superuser"
            ].help_text = "Você não pode tirar o seu próprio acesso."

    def clean_email(self):
        return _email_livre(self.cleaned_data["email"], self.instance)

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # O username acompanha o e-mail quando era o próprio e-mail
        if usuario.username == self.initial.get("email") or not usuario.pk:
            usuario.username = usuario.email
        usuario.is_staff = usuario.is_superuser
        if commit:
            usuario.save()
        return usuario


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


class SenhaUsuarioForm(_SenhaDupla):
    """Administrador define uma nova senha para o usuário."""

    def __init__(self, usuario, *args, **kwargs):
        self.usuario = usuario
        super().__init__(*args, **kwargs)

    def clean(self):
        dados = super().clean()
        self._confere_senha(self.usuario)
        return dados

    def save(self):
        self.usuario.set_password(self.cleaned_data["senha1"])
        self.usuario.save(update_fields=["password"])
        return self.usuario


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
