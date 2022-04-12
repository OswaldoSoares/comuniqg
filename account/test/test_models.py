import pytest

from ..models import Account

pytestmark = pytest.mark.django_db


def test_create_account():
    account = Account.objects.create_user(
        username="usuario_test", email="usuario@test.com", password="password"
    )
    assert account.username == "usuario_test"
    assert account.email == "usuario@test.com"
    assert account.is_active
    assert not account.is_staff
    assert not account.is_superuser


def test_create_superuser():
    account = Account.objects.create_superuser(
        username="admin_test", email="admin@test.com", password="password"
    )
    assert account.username == "admin_test"
    assert account.email == "admin@test.com"
    assert account.is_active
    assert account.is_staff
    assert account.is_superuser
