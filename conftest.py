import pytest

EMAIL_TESTE = "usuario.teste@example.com"
SENHA_TESTE = "Senha-Teste-123"


def pytest_configure(config):
    """Cria as tabelas legadas (databaseold) no banco de teste.

    Os models de databaseold são managed=False porque as tabelas pertencem
    ao app Delphi. Com --nomigrations (pytest.ini) o banco de teste é
    montado a partir dos models; marcá-los como gerenciados aqui faz o
    Django criar essas tabelas só no banco de teste. Não altera o código
    dos models nem o banco real.
    """
    from django.apps import apps

    for model in apps.get_app_config("databaseold").get_models():
        model._meta.managed = True


@pytest.fixture
def usuario(db, django_user_model):
    return django_user_model.objects.create_superuser(
        username="usuario_teste", email=EMAIL_TESTE, password=SENHA_TESTE
    )


@pytest.fixture
def client_logado(client, usuario):
    client.login(username=EMAIL_TESTE, password=SENHA_TESTE)
    return client
