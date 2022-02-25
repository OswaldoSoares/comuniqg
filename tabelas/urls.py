from unicodedata import name
from django.urls import path
from tabelas.views import index_tabela, delete_tabela, carrega_tabela, altera_valor_produto

urlpatterns = [
    path('', index_tabela, name='index_tabela'),
    path('delete_tabela/', delete_tabela, name='delete_tabela'),
    path('carrega_tabela/', carrega_tabela, name='carrega_tabela'),
    path('altera_valor_produto', altera_valor_produto, name='altera_valor_produto'),
]