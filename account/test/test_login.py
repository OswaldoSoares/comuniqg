import pytest
from django.urls import reverse

from conftest import EMAIL_TESTE, SENHA_TESTE

pytestmark = pytest.mark.django_db

TELAS_INTERNAS = [
    ("index_faturamento", None),
    ("cliente_faturada", None),
    ("cliente_faturar", None),
    ("print_fatura", [1]),
    ("servico_fatura", None),
    ("paga_fatura", None),
    ("seleciona_mes_recebido", None),
    ("seleciona_dia_recebido", None),
    ("seleciona_filtro_pagamento", None),
    ("faturar_selecionadas", None),
    ("index_tabela", None),
    ("altera_valor_produto", None),
    ("carrega_tabela", None),
    ("delete_tabela", None),
    ("delete_tabela_item", None),
    ("delete_zerado", None),
    ("nova_tabela_propria", None),
    ("novo_item_tabela", None),
    ("index_servico", None),
    ("print_servico", [1]),
    ("index_dashboard", None),
    ("index_clientes", None),
    ("pessoas_lista", None),
    ("pessoa_form", None),
]


def test_tela_de_login_abre(client):
    response = client.get(reverse("login"))
    assert response.status_code == 200
    assert "E-MAIL" in response.content.decode()


def test_login_valido_vai_para_servicos(client, usuario):
    response = client.post(
        reverse("login"), {"username": EMAIL_TESTE, "password": SENHA_TESTE}
    )
    assert response.status_code == 302
    assert response["Location"] == reverse("index_servico")


def test_login_invalido_mostra_erro(client, usuario):
    response = client.post(
        reverse("login"), {"username": EMAIL_TESTE, "password": "errada"}
    )
    assert response.status_code == 200
    assert "E-MAIL OU SENHA INVÁLIDOS." in response.content.decode()


def test_login_volta_para_a_tela_pedida(client, usuario):
    destino = reverse("index_tabela")
    response = client.post(
        reverse("login"),
        {"username": EMAIL_TESTE, "password": SENHA_TESTE, "next": destino},
    )
    assert response["Location"] == destino


def test_logado_nao_ve_o_login(client_logado):
    response = client_logado.get(reverse("login"))
    assert response.status_code == 302
    assert response["Location"] == reverse("index_servico")


def test_logout_volta_para_a_pagina_inicial(client_logado):
    response = client_logado.get(reverse("logout"))
    assert response["Location"] == reverse("index_core")
    response = client_logado.get(reverse("index_servico"))
    assert response["Location"].startswith(reverse("login"))


def test_pagina_inicial_e_aberta(client):
    assert client.get(reverse("index_core")).status_code == 200


@pytest.mark.parametrize("nome, args", TELAS_INTERNAS)
def test_tela_interna_exige_login(client, nome, args):
    url = reverse(nome, args=args)
    response = client.get(url)
    assert response.status_code == 302
    assert response["Location"] == f"{reverse('login')}?next={url}"
