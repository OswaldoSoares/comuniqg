from django.shortcuts import render
from tabelas.facade import carrega_cliente_tabela, context, delete_cliente_tabela, html_tabela_propria
from tabelas.facade import return_json, form_tabela
from tabelas.forms import FormAlteraValorProduto

def index_tabela(request):
    contexto = context()
    contexto_tipotb = {'tipotb': 'PRODUTO'}
    contexto.update(contexto_tipotb)
    return render(request, 'tabelas/index.html', contexto)


def delete_tabela(request):
    v_idcadastro = request.GET.get('idcadastro')
    data = dict()
    if delete_cliente_tabela(v_idcadastro):
        data = html_tabela_propria(request, data)
    data = return_json(data)
    return data


def carrega_tabela(request):
    v_idobj = request.GET.get('idcadastro')
    data = dict()
    data = carrega_cliente_tabela(request, v_idobj, data)
    data = return_json(data)
    return data


def altera_valor_produto(request):
    v_form = FormAlteraValorProduto
    v_idobj = request.GET.get('idobj')
    v_url = 'altera_valor_produto'
    v_view = 'altera_valor_produto'
    data = form_tabela(request, v_form, v_idobj, v_url, v_view)
    data = return_json(data)
    return data
