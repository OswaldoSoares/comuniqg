import pytest

from core import tools


@pytest.fixture
def mensagem_teste(monkeypatch):
    monkeypatch.setitem(
        tools.mensagens,
        "test0001",
        {"mensagem": "CLIENTE {apelido} ADICIONADO.", "tipo": "success"},
    )


def test_get_mensagem_codigo_inexistente():
    assert tools.get_mensagem("xxxx9999") == {
        "mensagem": "Mensagem não encontrada.",
        "tipo": "info",
    }


def test_get_mensagem_com_parametro(mensagem_teste):
    assert tools.get_mensagem("test0001", apelido="ACME") == {
        "mensagem": "CLIENTE ACME ADICIONADO.",
        "tipo": "success",
    }


def test_get_mensagem_parametro_ausente(mensagem_teste):
    resultado = tools.get_mensagem("test0001")
    assert "parâmetro ausente" in resultado["mensagem"]
    assert "apelido" in resultado["mensagem"]
    assert resultado["tipo"] == "success"
