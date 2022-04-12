import pytest
from account.models import Account
from databaseold.models import Receber


@pytest.mark.django_db
def test_count_fatura():
    assert Account.objects.count() == 0
