import pytest
from django.urls import reverse

from conftest import SENHA_TESTE

pytestmark = pytest.mark.django_db

NOVA = "Outra-Senha-789"


def test_sem_login_vai_para_o_login(client):
    response = client.get(reverse("minha_senha"))
    assert response.status_code == 302
    assert response["Location"].startswith(reverse("login"))


def test_tela_abre_com_os_tres_campos(client_logado):
    conteudo = client_logado.get(reverse("minha_senha")).content.decode()
    assert "SENHA ATUAL" in conteudo
    assert 'name="new_password1"' in conteudo
    assert 'name="new_password2"' in conteudo


def test_menu_tem_minha_senha(client_logado):
    conteudo = client_logado.get(reverse("index_servico")).content.decode()
    assert f'href="{reverse("minha_senha")}"' in conteudo


def test_troca_a_senha_e_continua_logado(client_logado, usuario, client):
    response = client_logado.post(
        reverse("minha_senha"),
        {
            "old_password": SENHA_TESTE,
            "new_password1": NOVA,
            "new_password2": NOVA,
        },
    )
    assert response["Location"] == reverse("minha_senha_ok")
    usuario.refresh_from_db()
    assert usuario.check_password(NOVA)
    # a sessão continua válida depois da troca
    assert client_logado.get(reverse("minha_senha_ok")).status_code == 200


def test_senha_atual_errada(client_logado, usuario):
    response = client_logado.post(
        reverse("minha_senha"),
        {
            "old_password": "errada",
            "new_password1": NOVA,
            "new_password2": NOVA,
        },
    )
    assert response.status_code == 200
    usuario.refresh_from_db()
    assert usuario.check_password(SENHA_TESTE)
    assert 'class="errorlist"' in response.content.decode()


def test_nova_senha_fraca(client_logado):
    response = client_logado.post(
        reverse("minha_senha"),
        {
            "old_password": SENHA_TESTE,
            "new_password1": "12345678",
            "new_password2": "12345678",
        },
    )
    assert response.status_code == 200
    assert 'class="errorlist"' in response.content.decode()


