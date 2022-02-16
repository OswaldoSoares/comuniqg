from django.urls import path
from tabelas.views import index_tabela

urlpatterns = [
    path('', index_tabela, name='index_tabela')
]