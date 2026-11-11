import pytest
from django.urls import reverse

from account.models import Account

pytestmark = pytest.mark.django_db

SENHA = "Senha-Nova-456"
URL_ADD = "admin:account_account_add"


def test_adicionar_usuario_pede_email(client_logado):
    conteudo = client_logado.get(reverse(URL_ADD)).content.decode()
    assert 'name="email"' in conteudo
    assert 'name="username"' not in conteudo


def test_adicionar_usuario_pelo_admin(client_logado, client):
    response = client_logado.post(
        reverse(URL_ADD),
        {
            "email": "Novo@Empresa.com.br",
            "password1": SENHA,
            "password2": SENHA,
        },
    )
    assert response.status_code == 302
    novo = Account.objects.get(email="novo@empresa.com.br")
    assert novo.username == "novo@empresa.com.br"
    assert not novo.is_superuser
    # o usuário criado já entra no sistema
    assert client.login(username="novo@empresa.com.br", password=SENHA)


def test_email_repetido_nao_entra(client_logado, usuario):
    response = client_logado.post(
        reverse(URL_ADD),
        {
            "email": usuario.email.upper(),
            "password1": SENHA,
            "password2": SENHA,
        },
    )
    assert response.status_code == 200
    assert "Já existe um usuário com este e-mail." in response.content.decode()


def test_lista_de_usuarios_abre(client_logado):
    response = client_logado.get(reverse("admin:account_account_changelist"))
    assert response.status_code == 200
