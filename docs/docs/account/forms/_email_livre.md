# `_email_livre`

Arquivo: `account/forms.py`

Normaliza o e-mail e recusa se outro usuário já o usa.

## Fluxo de Execução

1. Remove espaços e põe em minúsculas.
2. Procura o e-mail sem diferenciar maiúsculas, ignorando o próprio usuário na alteração.
3. Se achar, levanta `ValidationError`.

## Parâmetros

- `email` (`str`).
- `usuario` (`Account` ou `None`): Usuário em alteração.

## Retorno

- `str`: E-mail em minúsculas.

## Dependências

- `Account`.

## Código da Função

```{py3 linenums="1"}
def _email_livre(email, usuario=None):
    """E-mail em minúsculas, recusado se outro usuário já o usa."""
    email = email.strip().lower()
    repetido = Account.objects.filter(email__iexact=email)
    if usuario is not None and usuario.pk:
        repetido = repetido.exclude(pk=usuario.pk)
    if repetido.exists():
        raise ValidationError("Já existe um usuário com este e-mail.")
    return email
```

## Exemplo de Uso

```{py3 linenums="1"}
_email_livre(" Fulano@Empresa.com.br ")  # "fulano@empresa.com.br"
```
