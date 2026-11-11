# `SenhaUsuarioForm`

Arquivo: `account/forms.py`

O administrador define uma nova senha para um usuário (sem pedir a atual).

## Fluxo de Execução

1. Confere se as senhas são iguais e passa pelos validadores do Django.
2. `save` grava só o campo `password`.

## Parâmetros

- `usuario` (`Account`): Quem recebe a senha.
- `data` (`QueryDict`): `senha1` e `senha2`.

## Retorno

- `save()` retorna o `Account`.

## Dependências

- `_SenhaDupla`.

## Código da Função

```{py3 linenums="1"}
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
```

## Exemplo de Uso

```{py3 linenums="1"}
form = SenhaUsuarioForm(usuario, request.POST)
if form.is_valid():
    form.save()
```
