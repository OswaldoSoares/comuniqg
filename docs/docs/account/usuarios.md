# Usuários

O login é feito pelo **e-mail** e pela senha (`/account/login`). Não há tela de autocadastro: os usuários são criados pelo administrador.

## Criar pelo admin

1. Entrar em `/admin/` com um superusuário.
2. **Accounts → Adicionar**.
3. Informar o e-mail e a senha duas vezes e salvar.

O usuário já consegue entrar no sistema. Na tela seguinte dá para preencher o nome e marcar **Superusuário** (acesso ao admin e a todas as telas). O `username` recebe o próprio e-mail e não precisa ser mexido.

Para desativar alguém, desmarque **Ativo** em vez de excluir o usuário.

## Criar pelo terminal

```bash
poetry run python manage.py createsuperuser
```

O comando pede e-mail e senha. Para um usuário comum (sem acesso ao admin):

```bash
poetry run python manage.py shell -c "import getpass; from account.models import Account; Account.objects.create_user('fulano@empresa.com.br', getpass.getpass('Senha: '))"
```

## Produção

Em produção (servidor com Python 3.6), antes do primeiro usuário:

```bash
cd /comuniqg && source venv/bin/activate
PYTHONIOENCODING=utf-8 python manage.py migrate
PYTHONIOENCODING=utf-8 python manage.py createsuperuser
```

O `migrate` cria só as tabelas do Django (`account_account`, sessões, admin, permissões); as tabelas do Delphi têm `managed = False` e não mudam. O `PYTHONIOENCODING` é necessário porque o terminal do servidor é latin-1.

## Código

- [`AccountManager`](models/AccountManager.md): cria usuários pelo e-mail.
- [`AccountCreationForm`](forms/AccountCreationForm.md): formulário de adicionar usuário no admin.
- [`LoginForm`](forms/LoginForm.md): formulário de login.
