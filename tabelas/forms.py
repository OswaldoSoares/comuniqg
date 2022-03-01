from pyexpat import model
from django import forms
from databaseold.models import Produto


class FormAlteraValorProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = {'valor'}
        widgets = {'valor': forms.NumberInput(attrs={'class': 'form-control'}),
                   }
