# `UsuarioForm`

Arquivo: `account/forms.py`

Alterar usuário na tela de usuários: nome, sobrenome, e-mail e administrador.

## Fluxo de Execução

1. Nome é obrigatório; todos os campos recebem `form-control`.
2. Se quem edita (`editor`) é o próprio usuário, o campo administrador fica desabilitado: ninguém tira o próprio acesso.
3. `clean_email` usa `_email_livre`.
4. `save` atualiza o `username` quando ele era o e-mail antigo e deixa `is_staff` igual a `is_superuser` (administrador também entra no admin).

## Parâmetros

- `data` (`QueryDict`).
- `instance` (`Account`).
- `editor` (`Account`): Usuário logado.

## Retorno

- `save()` retorna o `Account`.

## Dependências

- [`_email_livre`](_email_livre.md).

## Código da Função

```{py3 linenums="1"}
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
```

## Exemplo de Uso

```{py3 linenums="1"}
form = UsuarioForm(request.POST, instance=usuario, editor=request.user)
```
