from django.http import JsonResponse
from databaseold.models import Tabela, Pessoa, Produto
from django.template.loader import render_to_string


def context():
    clientes = get_clientes()
    clientes_tabela = get_cliente_tabela()
    produtos_tabela = get_produto_tabela()
    context = {'clientes': clientes, 'clientes_tabela': clientes_tabela, 'produtos_tabela': produtos_tabela}
    return context


def get_clientes():
    clientes = Pessoa.objects.filter(funcao='CLIENTE')
    lista = [{'idpessoa': itens.idpessoa, 'apelido': itens.apelido} for itens in clientes]
    sorted_list = sorted(lista, key=lambda x: x['apelido'])
    return sorted_list


def get_tabela(id_cadastro):
    tabela = Tabela.objects.filter(idcadastro=id_cadastro)
    lista = [{'idtabela': itens.idtabela, 'idproduto': itens.idproduto__Descricao} for itens in tabela]
    return lista


def get_cliente_tabela():
    clientes = Tabela.objects.values('idcadastro').distinct()
    lista = []
    for x in clientes:
        search_cliente = Pessoa.objects.filter(idpessoa=x['idcadastro'])
        if search_cliente:
            lista.append({'idcadastro': x['idcadastro'], 'apelido': search_cliente[0].apelido})
    sorted_list = sorted(lista, key=lambda x: x['apelido'])
    return sorted_list


def get_produto_tabela():
    produtos = Produto.objects.all().order_by('categoria', 'descricao')
    lista = [{'idproduto': itens.idproduto, 'codigo': itens.codigo, 'descricao': itens.descricao,
             'categoria': itens.categoria, 'valor': itens.valor} for itens in produtos]
    return lista


def qs_get_produto(id_produto):
    produto = Produto.objects.get(idproduto=id_produto)
    return produto


def delete_cliente_tabela(id_cadastro):
    tabela = Tabela.objects.filter(idcadastro=id_cadastro)
    if tabela:
        tabela.delete()
        return True
    else:
        return False


def html_tabela_propria(request, data):
    contexto = context()
    data['html_tabela_propria'] = render_to_string('tabelas/tabela_propria.html', contexto, request=request)
    return data


def return_json(data):
    return JsonResponse(data)


def form_tabela(request, v_form, v_idobj, v_url, v_view):
    data = dict()
    v_instance = None
    if request.method == 'POST':
        if v_view == 'altera_valor_produto':
            v_idobj = request.POST.get('idproduto')
            v_instance = qs_get_produto(v_idobj)
            form = v_form(request.POST, instance=v_instance)
            if form.is_valid():
                form.save()
    else:
        if v_view == 'altera_valor_produto':
            v_instance = qs_get_produto(v_idobj)
        form = v_form(instance=v_instance)
    contexto = {'form': form, 'v_idobj': v_idobj, 'v_url': v_url, 'v_view': v_view}
    data['html_form'] = render_to_string('tabelas/form_tabelas.html', contexto, request=request)
    return data
