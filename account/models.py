from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class AccountManager(UserManager):
    """Cria usuários pelo e-mail, que é o login (USERNAME_FIELD).

    O Account herda o campo username (único e obrigatório) do Django;
    quando ele não é informado, recebe o próprio e-mail.
    """

    def _create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email).lower()
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        return super()._create_user(
            username or email, email, password, **extra_fields
        )

    def create_user(self, email=None, password=None, **extra_fields):
        username = extra_fields.pop("username", None)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        username = extra_fields.pop("username", None)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields["is_staff"] is not True:
            raise ValueError("Superusuário precisa de is_staff=True.")
        if extra_fields["is_superuser"] is not True:
            raise ValueError("Superusuário precisa de is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)


class Account(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # noqa: RUF012 (atributo do Django)

    objects = AccountManager()

    def __str__(self):
        return self.email
