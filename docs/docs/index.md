# Sistema ComuniQG

Sistema web (Django) que substitui aos poucos o aplicativo desktop em Delphi. Os dois usam **o mesmo banco MySQL** em produção.

## Regras do projeto

- **Não alterar a estrutura do banco legado** (tabelas do Delphi) enquanto o app desktop estiver em uso. As tabelas ficam em `databaseold/models.py`, todas com `managed = False`. Detalhes em [Banco legado](banco-legado.md).
- Tabelas novas do Django (`account_account`, sessões, permissões) podem ser criadas com `migrate`.
- O código precisa rodar em **Python 3.6** (produção). Em desenvolvimento usamos Python 3.11 com Poetry.
- Mesmo padrão do projeto efetiva:
  - views finas que chamam o `facade.py` do app;
  - `html_data.py` para renderizar os pedaços de HTML devolvidos por ajax;
  - mensagens em `core/message.py`, lidas por [`get_mensagem`](core/tools/get_mensagem.md);
  - visual `ui-*` ([Padrão visual](padrao-visual.md)).

## Módulos documentados

- [Clientes e fornecedores](clientes/index.md): o cadastro da tabela `pessoa`.
- [Usuários](account/usuarios.md): login por e-mail e como criar usuários (admin ou terminal).

## Produção

- Servidor com **Python 3.6.9**, projeto em `/comuniqg`, ambiente em `/comuniqg/venv`.
- **Não rode `pip install -r requirements.txt` no servidor**: ele tem versões de desenvolvimento que não existem para Python 3.6 (pylint 3, Pillow 10, ipython 8). Instale só o pacote que faltar, na versão do `requirements.txt`.
- Pacotes do sistema em produção: Django 3.1.3, django-decouple 2.1, **django-role-permissions 3.2.0** (compatível com Python 3.6), mysqlclient, Pillow 8.4 e reportlab 3.6.
- Comandos do `manage.py` com `PYTHONIOENCODING=utf-8` na frente, porque o terminal do servidor é latin-1.
- O sistema é servido pelo **Apache2 com mod_wsgi** em modo daemon (`/etc/apache2/sites-available/000-default.conf`), não pelo gunicorn do `Procfile`. Logs em `/comuniqg/site/logs/`.
- O Apache serve `/static` e `/media` direto de `/comuniqg/site/public/`, sem passar pelo Django. Por isso, a cada publicação que mexa em CSS, JS ou imagens, rode o `collectstatic`, senão as telas ficam sem os arquivos novos.

Para publicar, depois de atualizar o código em `/comuniqg` (com backup do banco antes, se houver migration):

```bash
cd /comuniqg && source venv/bin/activate
PYTHONIOENCODING=utf-8 python manage.py migrate
PYTHONIOENCODING=utf-8 python manage.py collectstatic --noinput
touch comuniqg/wsgi.py   # o mod_wsgi recarrega o código
```

## Comandos

```bash
poetry run python manage.py runserver   # sistema
poetry run pytest                       # testes
poetry run ruff check .                 # lint
```

## Documentação

```bash
pip install -r docs/requirements.txt
cd docs
mkdocs serve    # http://127.0.0.1:8000, recarrega ao salvar
mkdocs build    # gera docs/site/
```

Cada função tem uma página com descrição, fluxo de execução, parâmetros, retorno, dependências, código e exemplo de uso. Ao alterar uma função, atualize a página dela.
