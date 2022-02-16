from django.shortcuts import render
from tabelas.facade import context, get_cliente_tabela, delete_cliente_tabela

def index_tabela(request):
    contexto = context()
    return render(request, 'tabelas/index.html', contexto)


def delete_tabela(request):
    v_idcadastro = request.GET.get('idcadastro')
    delete_cliente_tabela(v_idcadastro)

