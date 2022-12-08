import pytest

from databaseold.models import Receber


@pytest.mark.django_db
def count_fatura():
    fatura = Receber.objects.create()
    assert fatura.idfatura == 38500
