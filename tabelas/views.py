from django.shortcuts import render
from tabelas.facade import context, get_cliente_tabela

def index_tabela(request):
    contexto = context()
    return render(request, 'tabelas/index.html', contexto)
