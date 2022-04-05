from django.contrib.auth import forms

from .models import Account


class AccountChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Account


class AccountCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Account
