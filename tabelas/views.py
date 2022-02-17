from django.shortcuts import render
from tabelas.facade import context, get_cliente_tabela, delete_cliente_tabela, html_tabela_propria, return_json

def index_tabela(request):
    contexto = context()
    return render(request, 'tabelas/index.html', contexto)


def delete_tabela(request):
    v_idcadastro = request.GET.get('idcadastro')
    data = dict()
    if delete_cliente_tabela(v_idcadastro):
        data = html_tabela_propria(request, data)
    data = return_json(data)
    return data
