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
- Login por e-mail: [`LoginForm`](account/forms/LoginForm.md).

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
