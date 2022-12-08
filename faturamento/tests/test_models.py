from databaseold.models import Receber
from faturamento.models import Fatura


def test_create_fatura(db):
    fatura = Fatura.objects.create(fatura=1)
    assert fatura.fatura == 1
