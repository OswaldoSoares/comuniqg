import pytest

from clientes.forms import MASCARA_ZERADA, CadastraPessoa
from databaseold.models import Pessoa

pytestmark = pytest.mark.django_db

CNPJ_VALIDO = "11.222.333/0001-81"
CPF_VALIDO = "529.982.247-25"


@pytest.fixture
def dados():
    return {
        "tipo": "J",
        "funcao": "CLIENTE",
        "apelido": "acme",
        "nome": "acme ltda",
    }


@pytest.fixture
def pessoa():
    return Pessoa.objects.create(
        apelido="EXISTENTE",
        nome="EXISTENTE LTDA",
        endereco="",
        bairro="",
        cidade="SÃO PAULO",
        estado="SP",
        cep=MASCARA_ZERADA["cep"],
        site="",
        cnpj=CNPJ_VALIDO,
        cpf=MASCARA_ZERADA["cpf"],
        ie=MASCARA_ZERADA["ie"],
        rg=MASCARA_ZERADA["rg"],
        ativo="S",
        funcao="CLIENTE",
    )


def test_minimo_valido_grava_no_formato_do_delphi(dados):
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
    pessoa = form.save()
    pessoa.refresh_from_db()
    assert pessoa.apelido == "ACME"
    assert pessoa.nome == "ACME LTDA"
    assert pessoa.ativo == "S"
    for campo, mascara in MASCARA_ZERADA.items():
        assert getattr(pessoa, campo) == mascara
    assert pessoa.endereco == ""
    assert pessoa.site == ""
    assert pessoa.obs is None


@pytest.mark.parametrize("campo", ["funcao", "apelido", "nome"])
def test_campos_obrigatorios(dados, campo):
    dados[campo] = ""
    form = CadastraPessoa(dados)
    assert not form.is_valid()
    assert campo in form.errors


def test_funcao_so_aceita_cliente_ou_fornecedor(dados):
    dados["funcao"] = "FUNCIONARIO"
    assert "funcao" in CadastraPessoa(dados).errors


def test_texto_em_maiusculas_e_sem_espacos_extras(dados):
    dados.update(
        {
            "nome": "  acme   comércio  ltda ",
            "cidade": "são paulo",
            "obs": "cliente antigo",
            "site": " WWW.Acme.COM.BR ",
        }
    )
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
    pessoa = form.save()
    assert pessoa.nome == "ACME COMÉRCIO LTDA"
    assert pessoa.cidade == "SÃO PAULO"
    assert pessoa.obs == "CLIENTE ANTIGO"
    assert pessoa.site == "www.acme.com.br"


def test_documentos_digitados_sem_mascara_sao_formatados(dados):
    dados.update(
        {"cnpj": "11222333000181", "cep": "03604010", "ie": "123456789012"}
    )
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
    pessoa = form.save()
    assert pessoa.cnpj == CNPJ_VALIDO
    assert pessoa.cep == "03604-010"
    assert pessoa.ie == "123.456.789.012"


def test_cpf_digitado_sem_mascara_e_formatado(dados):
    dados.update({"tipo": "F", "cpf": "52998224725"})
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
    assert form.save().cpf == CPF_VALIDO


def test_juridica_grava_cpf_e_rg_zerados(dados):
    # Campos do outro tipo ficam escondidos; se vierem, não são gravados
    dados.update({"cnpj": CNPJ_VALIDO, "cpf": "111.111.111-11", "rg": "123"})
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
    pessoa = form.save()
    assert pessoa.cnpj == CNPJ_VALIDO
    assert pessoa.cpf == MASCARA_ZERADA["cpf"]
    assert pessoa.rg == MASCARA_ZERADA["rg"]


def test_fisica_grava_cnpj_e_ie_zerados(dados):
    dados.update(
        {
            "tipo": "F",
            "cpf": CPF_VALIDO,
            "rg": "12.345.678-9",
            "cnpj": "11.111.111/1111-11",
            "ie": "isento",
        }
    )
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
    pessoa = form.save()
    assert pessoa.cpf == CPF_VALIDO
    assert pessoa.rg == "12.345.678-9"
    assert pessoa.cnpj == MASCARA_ZERADA["cnpj"]
    assert pessoa.ie == MASCARA_ZERADA["ie"]


def test_tipo_e_obrigatorio(dados):
    del dados["tipo"]
    assert "tipo" in CadastraPessoa(dados).errors


def test_novo_cadastro_comeca_como_juridica():
    assert CadastraPessoa().initial["tipo"] == "J"


@pytest.mark.parametrize(
    "documentos, funcao, esperado",
    [
        ({"cnpj": CNPJ_VALIDO}, "CLIENTE", "J"),
        ({"ie": "ISENTO"}, "FORNECEDOR", "J"),
        ({"cpf": CPF_VALIDO}, "CLIENTE", "F"),
        ({"rg": "12.345.678-9"}, "CLIENTE", "F"),
        ({}, "CLIENTE", "J"),
        ({}, "FORNECEDOR", "F"),
    ],
)
def test_edicao_deduz_o_tipo_pelos_documentos(
    pessoa, documentos, funcao, esperado
):
    pessoa.cnpj = MASCARA_ZERADA["cnpj"]
    pessoa.funcao = funcao
    for campo, valor in documentos.items():
        setattr(pessoa, campo, valor)
    assert CadastraPessoa(instance=pessoa).initial["tipo"] == esperado


@pytest.mark.parametrize(
    "campo, valor",
    [
        ("cnpj", "11.222.333/0001-82"),
        ("cnpj", "11.111.111/1111-11"),
        ("cpf", "529.982.247-24"),
        ("cpf", "111.111.111-11"),
        ("cep", "0360-401"),
    ],
)
def test_documento_invalido(dados, campo, valor):
    if campo == "cpf":
        dados["tipo"] = "F"
    dados[campo] = valor
    assert campo in CadastraPessoa(dados).errors


def test_ie_isento_fica_como_digitado(dados):
    dados["ie"] = "isento"
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
    assert form.save().ie == "ISENTO"


def test_apelido_repetido_nao_entra(dados, pessoa):
    dados["apelido"] = "existente"
    assert "apelido" in CadastraPessoa(dados).errors


def test_cnpj_repetido_nao_entra(dados, pessoa):
    dados["cnpj"] = CNPJ_VALIDO
    assert "cnpj" in CadastraPessoa(dados).errors


def test_cpf_repetido_nao_entra(dados, pessoa):
    pessoa.cpf = CPF_VALIDO
    pessoa.save()
    dados.update({"tipo": "F", "cpf": CPF_VALIDO})
    assert "cpf" in CadastraPessoa(dados).errors


def test_mascaras_zeradas_nao_contam_como_repetidas(dados, pessoa):
    # pessoa já tem CPF, IE, RG e CEP zerados
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors


def test_edicao_mantem_apelido_e_cnpj_da_propria_pessoa(pessoa):
    dados = {
        "tipo": "J",
        "funcao": "FORNECEDOR",
        "apelido": "existente",
        "nome": "novo nome",
        "cnpj": CNPJ_VALIDO,
    }
    form = CadastraPessoa(dados, instance=pessoa)
    assert form.is_valid(), form.errors
    alterada = form.save()
    assert alterada.pk == pessoa.pk
    assert alterada.funcao == "FORNECEDOR"
    assert alterada.nome == "NOVO NOME"


def test_edicao_mostra_mascara_zerada_como_vazio(pessoa):
    form = CadastraPessoa(instance=pessoa)
    assert form.initial["cpf"] == ""
    assert form.initial["cep"] == ""
    assert form.initial["cnpj"] == CNPJ_VALIDO


def test_edicao_nao_altera_ativo(pessoa):
    Pessoa.objects.filter(pk=pessoa.pk).update(ativo="N")
    pessoa.refresh_from_db()
    form = CadastraPessoa(
        {"tipo": "J", "funcao": "CLIENTE", "apelido": "EXISTENTE", "nome": "X"},
        instance=pessoa,
    )
    assert form.is_valid(), form.errors
    assert form.save().ativo == "N"


def test_novo_cadastro_sugere_sao_paulo():
    form = CadastraPessoa()
    assert form.initial["cidade"] == "SÃO PAULO"
    assert form.initial["estado"] == "SP"


@pytest.mark.parametrize(
    "texto",
    ["ACME 🚀", "ACME – LTDA", "“ACME”"],  # noqa: RUF001
)
def test_caractere_fora_do_latin1_e_recusado(dados, texto):
    dados["nome"] = texto
    form = CadastraPessoa(dados)
    assert "nome" in form.errors
    assert "Caractere não permitido" in form.errors["nome"][0]


def test_acentos_do_portugues_sao_aceitos(dados):
    dados["nome"] = "joão & cia. ação ç ü"
    form = CadastraPessoa(dados)
    assert form.is_valid(), form.errors
