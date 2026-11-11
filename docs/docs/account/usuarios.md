# Usuários

O login é feito pelo **e-mail** e pela senha (`/account/login`). Não há tela de autocadastro: os usuários são criados por um administrador.

## O que cada usuário acessa

- **Usuário comum**: todas as telas do sistema (serviços, faturamento, cadastro, tabelas) e a [minha senha](#minha-senha).
- **Administrador** (superusuário): também a [tela de usuários](#tela-de-usuarios) e o `/admin/`.

As telas usam `login_required`; só a tela de usuários usa [`administrador_required`](decorators/administrador_required.md). O pacote django-role-permissions continua instalado, mas nenhuma tela usa papéis; com `ROLEPERMISSIONS_REDIRECT_TO_LOGIN = False`, uma permissão que falte devolve 403 em vez de mandar para o login.

## Tela de usuários

Endereço `/account/usuarios/`, link **USUÁRIOS** no menu. Só administradores (superusuários) veem o link e abrem a tela; os outros recebem 403.

- **Lista** (esquerda): nome, e-mail e situação, com selo "Admin" para administradores. Filtros Ativos (padrão), Inativos e Todos, e busca por nome ou e-mail.
- **Detalhes** (direita): dados, data de cadastro e último acesso. Botões:
  - **alterar**: nome, sobrenome, e-mail e administrador;
  - **nova senha**: o administrador define uma senha nova, sem saber a atual (a antiga deixa de valer na hora);
  - **ativar / inativar**: inativo não consegue entrar. Inativar pede confirmação.
- **Novo usuário**: nome, sobrenome, e-mail, administrador e a senha duas vezes. O usuário já consegue entrar.

### Regras

- Não há excluir, só inativar, para preservar o histórico.
- Ninguém inativa o próprio usuário nem tira o próprio acesso de administrador, para não ficar trancado fora da tela.
- E-mail sem repetir (sem diferenciar maiúsculas), gravado em minúsculas.
- Senha: mínimo de 8 caracteres, não pode ser só números, uma senha comum ou parecida com o nome ou o e-mail (validadores do Django em `AUTH_PASSWORD_VALIDATORS`).
- Administrador ganha `is_superuser` e `is_staff` (acesso também ao `/admin/`).

### Endereços

| URL | View | Uso |
|---|---|---|
| `/account/usuarios/?filtro=&busca=&id_usuario=` | [`index_usuarios`](views/index_usuarios.md) | página |
| `/account/usuarios/lista` | [`usuarios_lista`](views/usuarios_lista.md) | lista e detalhes (JSON) |
| `/account/usuarios/consulta` | [`usuario_consulta`](views/usuario_consulta.md) | card de detalhes (JSON) |
| `/account/usuarios/form` | [`usuario_form`](views/usuario_form.md) | GET abre o modal, POST salva |
| `/account/usuarios/senha` | [`usuario_senha`](views/usuario_senha.md) | GET abre o modal, POST salva |
| `/account/usuarios/situacao` | [`usuario_situacao`](views/usuario_situacao.md) | POST ativa/inativa |

Mensagens em `core/message.py`: `acus0001` a `acus0006`.

## Minha senha

Endereço `/account/senha`, link **MINHA SENHA** no menu, para qualquer usuário logado. Pede a senha atual e a nova duas vezes; depois da troca o usuário continua logado e vê a confirmação em `/account/senha/ok`. Formulário: [`MinhaSenhaForm`](forms/MinhaSenhaForm.md).

## Outros caminhos

### Admin

Em `/admin/` → **Accounts → Adicionar**, com e-mail e senha ([`AccountCreationForm`](forms/AccountCreationForm.md)).

### Terminal

```bash
poetry run python manage.py createsuperuser
```

O comando pede e-mail e senha. Para um usuário comum:

```bash
poetry run python manage.py shell -c "import getpass; from account.models import Account; Account.objects.create_user('fulano@empresa.com.br', getpass.getpass('Senha: '))"
```

## Produção

Antes do primeiro usuário (servidor com Python 3.6):

```bash
cd /comuniqg && source venv/bin/activate
PYTHONIOENCODING=utf-8 python manage.py migrate
PYTHONIOENCODING=utf-8 python manage.py createsuperuser
```

O `migrate` cria só as tabelas do Django (`account_account`, sessões, admin, permissões); as tabelas do Delphi têm `managed = False` e não mudam. O `PYTHONIOENCODING` é necessário porque o terminal do servidor é latin-1.

Depois disso, os outros usuários são criados pela tela de usuários.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `account/models.py` | `Account` e [`AccountManager`](models/AccountManager.md) |
| `account/forms.py` | formulários de login, admin, tela de usuários e minha senha |
| `account/decorators.py` | [`administrador_required`](decorators/administrador_required.md) |
| `account/facade.py`, `account/html_data.py`, `account/views.py` | tela de usuários |
| `account/templates/account/` | login, usuários, modais e minha senha |
| `core/static/core/js/usuarios.js` | [comportamento da tela](javascript.md) |
| `core/static/core/css/usuarios.css` | selos e minha senha (a base vem de `ui-cadastro.css`) |
| `account/test/` | testes |
