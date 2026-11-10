import pytest
from django.urls import reverse

from clientes import facade
from clientes.forms import MASCARA_ZERADA
from databaseold.models import Pessoa

pytestmark = pytest.mark.django_db


def cria_pessoa(apelido, funcao="CLIENTE", **campos):
    dados = {
        "apelido": apelido,
        "nome": f"{apelido} LTDA",
        "endereco": "",
        "bairro": "",
        "cidade": "SÃO PAULO",
        "estado": "SP",
        "site": "",
        "ativo": "S",
        "funcao": funcao,
        **MASCARA_ZERADA,
    }
    dados.update(campos)
    return Pessoa.objects.create(**dados)


@pytest.fixture
def pessoas():
    return [
        cria_pessoa("ACME", cnpj="11.222.333/0001-81"),
        cria_pessoa("BETA"),
        cria_pessoa("GRAFICA", funcao="FORNECEDOR", cpf="529.982.247-25"),
    ]


def apelidos(contexto):
    return [p.apelido for p in contexto["pessoas"]]


# --- facade ----------------------------------------------------------------


def test_lista_padrao_mostra_so_clientes(pessoas):
    assert apelidos(facade.create_contexto_pessoas()) == ["ACME", "BETA"]


def test_filtro_fornecedor_e_todos(pessoas):
    assert apelidos(facade.create_contexto_pessoas("FORNECEDOR")) == [
        "GRAFICA"
    ]
    assert apelidos(facade.create_contexto_pessoas("TODOS")) == [
        "ACME",
        "BETA",
        "GRAFICA",
    ]


def test_filtro_invalido_volta_para_clientes():
    assert facade.obter_filtro("qualquer") == "CLIENTE"
    assert facade.obter_filtro("fornecedor") == "FORNECEDOR"


@pytest.mark.parametrize(
    "busca, esperado",
    [
        ("acm", ["ACME"]),
        ("beta ltda", ["BETA"]),
        ("11.222", ["ACME"]),
        ("11222333", ["ACME"]),
        ("52998", ["GRAFICA"]),
        ("zzz", []),
    ],
)
def test_busca_por_apelido_nome_e_documento(pessoas, busca, esperado):
    contexto = facade.create_contexto_pessoas("TODOS", busca)
    assert apelidos(contexto) == esperado


def test_documento_mostra_o_que_estiver_preenchido(pessoas):
    acme, beta, grafica = pessoas
    assert facade.documento(acme) == "11.222.333/0001-81"
    assert facade.documento(beta) == ""
    assert facade.documento(grafica) == "529.982.247-25"


# --- views -----------------------------------------------------------------


def test_menu_tem_link_do_cadastro(client_logado):
    response = client_logado.get(reverse("index_servico"))
    assert f'href="{reverse("index_clientes")}"' in response.content.decode()


def test_tela_do_cadastro_abre(client_logado, pessoas):
    response = client_logado.get(reverse("index_clientes"))
    conteudo = response.content.decode()
    assert response.status_code == 200
    assert "Clientes e fornecedores" in conteudo
    assert "ACME" in conteudo
    assert "GRAFICA" not in conteudo


def test_lista_por_ajax(client_logado, pessoas):
    response = client_logado.get(
        reverse("pessoas_lista"), {"filtro": "FORNECEDOR", "busca": ""}
    )
    data = response.json()
    assert data["filtro"] == "FORNECEDOR"
    assert "GRAFICA" in data["html-card-pessoas"]
    assert "ACME" not in data["html-card-pessoas"]


def test_get_form_novo_abre_o_modal(client_logado):
    data = client_logado.get(reverse("pessoa_form")).json()
    assert 'name="apelido"' in data["modal_html"]
    assert '<option value="J" selected>JURÍDICA</option>' in data["modal_html"]
    assert 'data-tipo="J"' in data["modal_html"]
    assert 'data-tipo="F"' in data["modal_html"]
    assert 'name="id_pessoa"' not in data["modal_html"]


def test_get_form_edicao_traz_a_pessoa(client_logado, pessoas):
    acme = pessoas[0]
    data = client_logado.get(
        reverse("pessoa_form"), {"id_pessoa": acme.pk}
    ).json()
    assert f'value="{acme.pk}"' in data["modal_html"]
    assert 'value="ACME"' in data["modal_html"]


def test_post_valido_adiciona_e_devolve_a_lista(client_logado, pessoas):
    response = client_logado.post(
        reverse("pessoa_form"),
        {
            "tipo": "F",
            "funcao": "FORNECEDOR",
            "apelido": "papelaria",
            "nome": "papelaria central",
            "filtro": "CLIENTE",
        },
    )
    data = response.json()
    assert Pessoa.objects.filter(apelido="PAPELARIA").exists()
    assert data["mensagem"] == "FORNECEDOR PAPELARIA ADICIONADO COM SUCESSO."
    assert data["tipo"] == "success"
    # vai para a lista de fornecedores, onde o novo cadastro aparece
    assert data["filtro"] == "FORNECEDOR"
    assert "PAPELARIA" in data["html-card-pessoas"]


def test_post_invalido_devolve_o_form_com_erros(client_logado, pessoas):
    response = client_logado.post(
        reverse("pessoa_form"),
        {"funcao": "CLIENTE", "apelido": "acme", "nome": "outra"},
    )
    data = response.json()
    assert "html_form" in data
    assert "Já existe um cadastro com este apelido." in data["html_form"]
    assert Pessoa.objects.filter(apelido="ACME").count() == 1


def test_post_edicao_altera(client_logado, pessoas):
    beta = pessoas[1]
    response = client_logado.post(
        reverse("pessoa_form"),
        {
            "id_pessoa": beta.pk,
            "tipo": "J",
            "funcao": "CLIENTE",
            "apelido": "beta",
            "nome": "beta nova",
            "filtro": "TODOS",
        },
    )
    data = response.json()
    beta.refresh_from_db()
    assert beta.nome == "BETA NOVA"
    assert data["mensagem"] == "CLIENTE BETA ALTERADO COM SUCESSO."
    assert data["filtro"] == "TODOS"


def test_edicao_de_pessoa_inexistente_da_404(client_logado):
    response = client_logado.get(reverse("pessoa_form"), {"id_pessoa": 999})
    assert response.status_code == 404
