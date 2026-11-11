from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account


@admin.register(Account)
class AccountAdmin(auth_admin.UserAdmin):
    """Usuários do sistema, identificados pelo e-mail."""

    form = AccountChangeForm
    add_form = AccountCreationForm
    model = Account

    # Adicionar usuário: e-mail e senha (o username recebe o e-mail)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
