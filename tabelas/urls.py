from unicodedata import name
from django.urls import path
from tabelas.views import altera_valor_produto, carrega_tabela, delete_tabela, delete_tabela_item, delete_zerado, index_tabela, nova_tabela_propria, novo_item_tabela

urlpatterns = [
    path('', index_tabela, name='index_tabela'),
    path('altera_valor_produto', altera_valor_produto, name='altera_valor_produto'),
    path('carrega_tabela/', carrega_tabela, name='carrega_tabela'),
    path('delete_tabela/', delete_tabela, name='delete_tabela'),
    path('delete_tabela_item/', delete_tabela_item, name='delete_tabela_item'),
    path('delete_zerado/', delete_zerado, name='delete_zerado'),
    path('nova_tabela_propria', nova_tabela_propria, name='nova_tabela_propria'),
    path('novo_item_tabela/', novo_item_tabela, name='novo_item_tabela'),
]