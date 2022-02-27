from pyexpat import model
from django import forms
from databaseold.models import Produto, Tabela, Pessoa


class FormAlteraValorProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = {'valor'}
        widgets = {'valor': forms.NumberInput(attrs={'class': 'form-control'}),
                   }


class FormNovaTabelaPropria(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = {'apelido'}
        widgets = {'apelido': forms.Select(attrs={'class': 'form-control'}),
                   }
