import pytest

from account.forms import NovoUsuarioForm, SenhaUsuarioForm, UsuarioForm
from account.models import Account

pytestmark = pytest.mark.django_db

SENHA = "Senha-Nova-456"


@pytest.fixture
def comum(db):
    return Account.objects.create_user(
        "comum@empresa.com.br", SENHA, first_name="Maria"
    )


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


# --- formulários -------------------------------------------------------------


def test_novo_usuario_grava_pelo_email():
    form = NovoUsuarioForm(novo())
    assert form.is_valid(), form.errors
    usuario = form.save()
    assert usuario.email == "joao@empresa.com.br"
    assert usuario.username == "joao@empresa.com.br"
    assert usuario.check_password(SENHA)
    assert not usuario.is_superuser
    assert not usuario.is_staff


def test_novo_administrador_tambem_acessa_o_admin():
    usuario = NovoUsuarioForm(novo(is_superuser="True"))
    assert usuario.is_valid(), usuario.errors
    usuario = usuario.save()
    assert usuario.is_superuser
    assert usuario.is_staff


@pytest.mark.parametrize(
    "campos, campo_com_erro",
    [
        ({"senha2": "Outra-Senha-789"}, "senha2"),
        ({"senha1": "12345678", "senha2": "12345678"}, "senha1"),
        ({"senha1": "curta", "senha2": "curta"}, "senha1"),
        ({"first_name": ""}, "first_name"),
        ({"email": "invalido"}, "email"),
    ],
)
def test_novo_usuario_recusa(campos, campo_com_erro):
    assert campo_com_erro in NovoUsuarioForm(novo(**campos)).errors


def test_email_repetido(comum):
    form = NovoUsuarioForm(novo(email="COMUM@empresa.com.br"))
    assert "email" in form.errors


def test_alteracao_atualiza_username_junto_com_o_email(comum):
    form = UsuarioForm(
        {"first_name": "Maria", "email": "maria@empresa.com.br"},
        instance=comum,
    )
    assert form.is_valid(), form.errors
    alterado = form.save()
    assert alterado.username == "maria@empresa.com.br"
    assert alterado.check_password(SENHA)  # a senha não muda


def test_proprio_usuario_nao_tira_seu_acesso(usuario):
    form = UsuarioForm(
        {"first_name": "Eu", "email": usuario.email, "is_superuser": "False"},
        instance=usuario,
        editor=usuario,
    )
    assert form.is_valid(), form.errors
    assert form.save().is_superuser


def test_nova_senha(comum):
    form = SenhaUsuarioForm(
        comum, {"senha1": "Outra-Senha-789", "senha2": "Outra-Senha-789"}
    )
    assert form.is_valid(), form.errors
    form.save()
    comum.refresh_from_db()
    assert comum.check_password("Outra-Senha-789")
