import datetime

import pytest
from django.urls import reverse

from clientes import facade
from clientes.forms import MASCARA_ZERADA
from databaseold.models import Contato, Pessoa, Servico

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


@pytest.mark.parametrize(
    "valor, esperado",
    [
        ("000.000.000-00", ""),
        ("00.000.000/0000-00", ""),
        ("(00)00000-0000", ""),
        ("00000-000", ""),
        ("", ""),
        (None, ""),
        ("01310-100", "01310-100"),
        ("ISENTO", "ISENTO"),
    ],
)
def test_mascara_zerada_nao_aparece_no_detalhe(valor, esperado):
    assert facade.preenchido(valor) == esperado


def cria_contato(pessoa, nome, **campos):
    dados = {
        "idpessoa": pessoa.pk,
        "contato": nome,
        "telefone1": "(00)00000-0000",
        "telefone2": "(00)00000-0000",
        "celular1": "(00)00000-0000",
        "celular2": "(00)00000-0000",
        "radio": "",
        "email": "",
        "nascimento": datetime.date(2012, 1, 1),
    }
    dados.update(campos)
    return Contato.objects.create(**dados)


def cria_servico(pessoa, idservico, dia):
    return Servico.objects.create(
        idservico=idservico,
        idcadastro=pessoa.pk,
        diaservico=dia,
        total=0,
        idfatura=0,
        status="ABERTO",
        obra="",
        diaentrega=dia,
        solicitante="",
        seleciona="N",
        checkin=0,
    )


def test_detalhe_do_cliente(pessoas):
    acme = pessoas[0]
    cria_contato(acme, "JOAO", celular1="(11)91234-5678")
    cria_servico(acme, 1, datetime.date(2026, 1, 5))
    cria_servico(acme, 2, datetime.date(2026, 3, 9))

    contexto = facade.create_contexto_pessoa(acme.pk)

    dados = dict(contexto["dados"])
    assert dados["CNPJ"] == "11.222.333/0001-81"
    assert dados["CPF"] == ""
    assert dados["Cidade"] == "SÃO PAULO/SP"
    assert contexto["contatos"] == [
        {"nome": "JOAO", "fones": ["(11)91234-5678"], "email": ""}
    ]
    assert contexto["movimento"]["rotulo"] == "Serviços"
    assert contexto["movimento"]["quantidade"] == 2
    assert contexto["movimento"]["ultimo"] == datetime.date(2026, 3, 9)


def test_detalhe_do_fornecedor_conta_contas_a_pagar(pessoas):
    grafica = pessoas[2]
    movimento = facade.create_contexto_pessoa(grafica.pk)["movimento"]
    assert movimento["rotulo"] == "Contas a pagar"
    assert movimento["quantidade"] == 0
    assert movimento["ultimo"] is None


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


def test_lista_mostra_so_apelido_nome_e_funcao(client_logado, pessoas):
    conteudo = client_logado.get(reverse("index_clientes")).content.decode()
    assert "11.222.333/0001-81" not in conteudo
    assert "<th>Documento</th>" not in conteudo
    assert "<th>Cidade</th>" not in conteudo
    assert "Selecione um cadastro na lista" in conteudo


def test_tela_abre_com_a_pessoa_do_link(client_logado, pessoas):
    acme = pessoas[0]
    response = client_logado.get(
        reverse("index_clientes"), {"id_pessoa": acme.pk}
    )
    conteudo = response.content.decode()
    assert "11.222.333/0001-81" in conteudo
    assert "ui-linha-ativa" in conteudo


def test_consulta_devolve_o_card_da_pessoa(client_logado, pessoas):
    acme = pessoas[0]
    data = client_logado.get(
        reverse("pessoa_consulta"), {"id_pessoa": acme.pk}
    ).json()
    assert "11.222.333/0001-81" in data["html-card-pessoa"]
    assert "ALTERAR CLIENTE ACME" in data["html-card-pessoa"]


def test_consulta_de_pessoa_inexistente_da_404(client_logado):
    response = client_logado.get(reverse("pessoa_consulta"), {"id_pessoa": 999})
    assert response.status_code == 404


def test_lista_mantem_a_pessoa_selecionada(client_logado, pessoas):
    acme = pessoas[0]
    data = client_logado.get(
        reverse("pessoas_lista"),
        {"filtro": "CLIENTE", "busca": "", "id_pessoa": acme.pk},
    ).json()
    assert data["id_pessoa"] == acme.pk
    assert "ui-linha-ativa" in data["html-card-pessoas"]
    assert "11.222.333/0001-81" in data["html-card-pessoa"]


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
    # e já abre o novo cadastro no card de detalhes
    novo = Pessoa.objects.get(apelido="PAPELARIA")
    assert data["id_pessoa"] == novo.pk
    assert "ALTERAR FORNECEDOR PAPELARIA" in data["html-card-pessoa"]


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


def test_lista_sem_selecao_volta_o_card_vazio(client_logado, pessoas):
    # Ao trocar o filtro a tela não manda id_pessoa
    data = client_logado.get(
        reverse("pessoas_lista"), {"filtro": "FORNECEDOR", "id_pessoa": ""}
    ).json()
    assert data["id_pessoa"] == ""
    assert "ui-linha-ativa" not in data["html-card-pessoas"]
    assert "Selecione um cadastro na lista" in data["html-card-pessoa"]
