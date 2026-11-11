import pytest
from django.test import Client
from django.urls import reverse

from account.models import Account

pytestmark = pytest.mark.django_db

SENHA = "Senha-Nova-456"


@pytest.fixture
def comum(db):
    return Account.objects.create_user(
        "comum@empresa.com.br", SENHA, first_name="Maria"
    )


@pytest.fixture
def client_comum(comum):
    # Cliente próprio: o fixture client é o mesmo do client_logado
    cliente = Client()
    cliente.login(username=comum.email, password=SENHA)
    return cliente


def novo(**campos):
    dados = {
        "first_name": "joão",
        "last_name": "silva",
        "email": "Joao@Empresa.com.br",
        "is_superuser": "False",
        "senha1": SENHA,
        "senha2": SENHA,
    }
    dados.update(campos)
    return dados


# --- permissões --------------------------------------------------------------

TELAS = [
    ("index_usuarios", "get"),
    ("usuarios_lista", "get"),
    ("usuario_consulta", "get"),
    ("usuario_form", "get"),
    ("usuario_senha", "get"),
    ("usuario_situacao", "post"),
]


@pytest.mark.parametrize("nome, metodo", TELAS)
def test_sem_login_vai_para_o_login(client, nome, metodo):
    response = getattr(client, metodo)(reverse(nome))
    assert response.status_code == 302
    assert response["Location"].startswith(reverse("login"))


@pytest.mark.parametrize("nome, metodo", TELAS)
def test_usuario_comum_e_barrado(client_comum, nome, metodo):
    assert getattr(client_comum, metodo)(reverse(nome)).status_code == 403


def test_menu_mostra_usuarios_so_para_administrador(
    client_logado, client_comum
):
    link = f'href="{reverse("index_usuarios")}"'
    assert link in client_logado.get(reverse("index_servico")).content.decode()
    assert (
        link not in client_comum.get(reverse("index_servico")).content.decode()
    )


# --- tela ------------------------------------------------------------------


def test_tela_lista_os_ativos(client_logado, comum):
    comum.is_active = False
    comum.save()
    conteudo = client_logado.get(reverse("index_usuarios")).content.decode()
    assert "Usuários" in conteudo
    assert "comum@empresa.com.br" not in conteudo
    assert "Selecione um usuário na lista" in conteudo
    assert 'name="csrfmiddlewaretoken"' in conteudo


def test_busca_e_filtro(client_logado, comum):
    data = client_logado.get(
        reverse("usuarios_lista"), {"filtro": "TODOS", "busca": "maria"}
    ).json()
    assert "comum@empresa.com.br" in data["html-card-usuarios"]
    assert data["id_usuario"] == ""


def test_consulta_mostra_o_card(client_logado, comum):
    data = client_logado.get(
        reverse("usuario_consulta"), {"id_usuario": comum.pk}
    ).json()
    assert "ALTERAR USUÁRIO comum@empresa.com.br" in data["html-card-usuario"]
    assert "Nunca entrou" in data["html-card-usuario"]


def test_novo_usuario_pela_tela(client_logado, client):
    data = client_logado.post(
        reverse("usuario_form"), {**novo(), "filtro": "ATIVOS"}
    ).json()
    assert data["mensagem"] == (
        "USUÁRIO joao@empresa.com.br ADICIONADO COM SUCESSO."
    )
    joao = Account.objects.get(email="joao@empresa.com.br")
    assert data["id_usuario"] == joao.pk
    assert client.login(username="joao@empresa.com.br", password=SENHA)


def test_form_com_erro_volta_para_o_modal(client_logado):
    data = client_logado.post(
        reverse("usuario_form"), novo(senha2="diferente")
    ).json()
    assert "As senhas não conferem." in data["html_form"]


def test_alterar_pela_tela(client_logado, comum):
    data = client_logado.post(
        reverse("usuario_form"),
        {
            "id_usuario": comum.pk,
            "first_name": "Maria",
            "last_name": "Souza",
            "email": comum.email,
            "is_superuser": "False",
        },
    ).json()
    comum.refresh_from_db()
    assert comum.last_name == "Souza"
    assert data["tipo"] == "success"


def test_modal_de_alteracao_nao_tem_senha(client_logado, comum):
    html = client_logado.get(
        reverse("usuario_form"), {"id_usuario": comum.pk}
    ).json()["modal_html"]
    assert 'name="senha1"' not in html
    assert 'value="comum@empresa.com.br"' in html


def test_nova_senha_pela_tela(client_logado, comum, client):
    data = client_logado.post(
        reverse("usuario_senha"),
        {
            "id_usuario": comum.pk,
            "senha1": "Outra-Senha-789",
            "senha2": "Outra-Senha-789",
        },
    ).json()
    assert data["mensagem"] == (
        "SENHA DE comum@empresa.com.br ALTERADA COM SUCESSO."
    )
    assert client.login(username=comum.email, password="Outra-Senha-789")


def test_trocar_a_propria_senha_mantem_o_login(client_logado, usuario):
    client_logado.post(
        reverse("usuario_senha"),
        {
            "id_usuario": usuario.pk,
            "senha1": "Outra-Senha-789",
            "senha2": "Outra-Senha-789",
        },
    )
    assert client_logado.get(reverse("index_usuarios")).status_code == 200


def test_inativar_e_ativar(client_logado, comum, client):
    data = client_logado.post(
        reverse("usuario_situacao"),
        {"id_usuario": comum.pk, "filtro": "ATIVOS"},
    ).json()
    comum.refresh_from_db()
    assert not comum.is_active
    assert data["tipo"] == "warning"
    # inativo some de "Ativos": a lista passa para "Todos"
    assert data["filtro"] == "TODOS"
    assert not client.login(username=comum.email, password=SENHA)

    client_logado.post(reverse("usuario_situacao"), {"id_usuario": comum.pk})
    comum.refresh_from_db()
    assert comum.is_active


def test_nao_inativa_a_si_mesmo(client_logado, usuario):
    data = client_logado.post(
        reverse("usuario_situacao"), {"id_usuario": usuario.pk}
    ).json()
    usuario.refresh_from_db()
    assert usuario.is_active
    assert data["mensagem"] == "VOCÊ NÃO PODE INATIVAR O SEU PRÓPRIO USUÁRIO."


def test_card_do_proprio_usuario_nao_tem_inativar(client_logado, usuario):
    html = client_logado.get(
        reverse("usuario_consulta"), {"id_usuario": usuario.pk}
    ).json()["html-card-usuario"]
    assert "js-usuario-situacao" not in html
    assert "· você" in html
