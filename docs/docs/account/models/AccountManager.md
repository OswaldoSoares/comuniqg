# `AccountManager`

Arquivo: `account/models.py`

Gerenciador do `Account` (`Account.objects`). Cria usuários pelo e-mail, que é o login (`USERNAME_FIELD`). O campo `username`, herdado do Django e único, recebe o próprio e-mail quando não é informado.

## Fluxo de Execução

1. `create_user` e `create_superuser` tiram `username` dos argumentos (opcional).
2. `create_superuser` liga `is_staff` e `is_superuser`.
3. `_create_user` põe o e-mail em minúsculas, recusa e-mail vazio e usa o e-mail como `username` quando ele não veio.
4. O `UserManager` do Django grava o usuário com a senha criptografada.

## Parâmetros

- `email` (`str`): Login do usuário.
- `password` (`str`).
- `**extra_fields`: `username`, `first_name`, `is_active` etc.

## Retorno

- `Account` gravado.

## Dependências

- `django.contrib.auth.models.UserManager`.
- Migração `account 0003_account_manager` (só registra o gerenciador, sem SQL).

## Código da Função

```{py3 linenums="1"}
class AccountManager(UserManager):
    """Cria usuários pelo e-mail, que é o login (USERNAME_FIELD).

    O Account herda o campo username (único e obrigatório) do Django;
    quando ele não é informado, recebe o próprio e-mail.
    """

    def _create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email).lower()
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        return super()._create_user(
            username or email, email, password, **extra_fields
        )

    def create_user(self, email=None, password=None, **extra_fields):
        username = extra_fields.pop("username", None)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        username = extra_fields.pop("username", None)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields["is_staff"] is not True:
            raise ValueError("Superusuário precisa de is_staff=True.")
        if extra_fields["is_superuser"] is not True:
            raise ValueError("Superusuário precisa de is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)
```

## Exemplo de Uso

```{py3 linenums="1"}
Account.objects.create_user("fulano@empresa.com.br", "senha")
Account.objects.create_superuser("admin@empresa.com.br", "senha")
# python manage.py createsuperuser  -> pede e-mail e senha
```
