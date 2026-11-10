import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_menu_tem_link_do_cadastro(client_logado):
    response = client_logado.get(reverse("index_servico"))
    assert f'href="{reverse("index_clientes")}"' in response.content.decode()


def test_tela_do_cadastro_abre(client_logado):
    response = client_logado.get(reverse("index_clientes"))
    assert response.status_code == 200
    assert "Clientes e fornecedores" in response.content.decode()
