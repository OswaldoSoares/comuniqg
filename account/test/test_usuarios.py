import pytest
from django.core.management import call_command

from account.models import Account

pytestmark = pytest.mark.django_db

SENHA = "Senha-Teste-123"


def test_create_user_pelo_email():
    usuario = Account.objects.create_user("Fulano@Empresa.com.br", SENHA)
    assert usuario.email == "fulano@empresa.com.br"
    assert usuario.username == "fulano@empresa.com.br"
    assert usuario.check_password(SENHA)
    assert not usuario.is_staff
    assert not usuario.is_superuser


def test_create_user_aceita_username():
    usuario = Account.objects.create_user(
        "fulano@empresa.com.br", SENHA, username="fulano"
    )
    assert usuario.username == "fulano"


def test_create_user_exige_email():
    with pytest.raises(ValueError):
        Account.objects.create_user("", SENHA)


def test_create_superuser():
    usuario = Account.objects.create_superuser("admin@empresa.com.br", SENHA)
    assert usuario.is_staff
    assert usuario.is_superuser


def test_createsuperuser_cria_mais_de_um(monkeypatch):
    # Antes do AccountManager o comando falhava pedindo username
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", SENHA)
    for email in ("a@empresa.com.br", "b@empresa.com.br"):
        call_command("createsuperuser", "--noinput", "--email", email)
    assert Account.objects.filter(is_superuser=True).count() == 2


def test_usuario_criado_faz_login(client):
    Account.objects.create_user("fulano@empresa.com.br", SENHA)
    assert client.login(username="fulano@empresa.com.br", password=SENHA)
