from django.shortcuts import render
from tabelas.facade import carrega_cliente_tabela, carrega_produto_tabela, context, delete_cliente_tabela, form_exclui, return_json, form_tabela, html_tabela_propria, delete_itens_zerados, get_produto_no_tabela
from tabelas.forms import FormAlteraValorProduto, FormNovaTabelaPropria


def altera_valor_produto(request):
    v_form = FormAlteraValorProduto
    v_idobj = request.GET.get('idobj')
    v_url = 'altera_valor_produto'
    v_view = 'altera_valor_produto'
    data = form_tabela(request, v_form, v_idobj, v_url, v_view)
    data = return_json(data)
    return data


def carrega_tabela(request):
    v_idobj = request.GET.get('idcadastro')
    data = dict()
    data = carrega_cliente_tabela(request, v_idobj, data)
    data = return_json(data)
    return data


def delete_tabela(request):
    v_idcadastro = request.GET.get('idcadastro')
    data = dict()
    if delete_cliente_tabela(v_idcadastro):
        data = html_tabela_propria(request, data)
    data = carrega_produto_tabela(request, data)
    data = return_json(data)
    return data


def delete_tabela_item(request):
    v_idobj = request.GET.get('idobj')
    v_view = 'delete_tabela_item'
    data = form_exclui(request, v_idobj, v_view)
    data = return_json(data)
    return data


def delete_zerado(request):
    v_idobj = request.GET.get('idobj')
    data = delete_itens_zerados(request, v_idobj)
    data = return_json(data)
    return data
    

def index_tabela(request):
    contexto = context()
    contexto_tipotb = {'tipotb': 'PRODUTO'}
    contexto.update(contexto_tipotb)
    return render(request, 'tabelas/index.html', contexto)


def nova_tabela_propria(request):
    v_form = FormNovaTabelaPropria
    v_idobj = ''
    v_url = 'nova_tabela_propria'
    v_view = 'nova_tabela_propria'
    data = form_tabela(request, v_form, v_idobj, v_url, v_view)
    data['idcadastro'] = request.POST.get('cliente')
    data['nova_tabela'] = True
    data = return_json(data)
    return data


def novo_item_tabela(request):
    print(request.POST)
    v_form = None
    v_idobj = request.GET.get('idobj')
    v_url = 'novo_item_tabela/'
    v_view = 'novo_item_tabela'
    data = form_tabela(request, v_form, v_idobj, v_url, v_view)
    data = return_json(data)
    return data
