from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from pyexpat import model

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account


@admin.register(Account)
class AccountAdmin(auth_admin.UserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    model = Account
