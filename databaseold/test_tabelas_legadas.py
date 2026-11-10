import pytest

from databaseold.models import Pessoa

pytestmark = pytest.mark.django_db


def test_tabela_pessoa_existe_no_banco_de_teste():
    """O conftest.py cria as tabelas legadas só no banco de teste."""
    Pessoa.objects.create(
        apelido="ACME",
        nome="ACME LTDA",
        endereco="",
        bairro="",
        cidade="",
        estado="SP",
        cep="",
        site="",
        cnpj="",
        cpf="",
        ie="",
        rg="",
        ativo="S",
        funcao="CLIENTE",
    )
    assert Pessoa.objects.filter(funcao="CLIENTE").count() == 1
