from multiprocessing.dummy import connection
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


def get_cliente_no_tabela():
    clientes_tabela = get_cliente_tabela()
    lista_idpessoa = []
    for x in clientes_tabela:
        lista_idpessoa.append(x['idcadastro'])
    clientes_no_tabela = Pessoa.objects.filter(funcao='CLIENTE').exclude(idpessoa__in=lista_idpessoa)
    lista = [{'idpessoa': itens.idpessoa, 'apelido': itens.apelido} for itens in clientes_no_tabela]
    sorted_list = sorted(lista, key=lambda x: x['apelido'])
    return sorted_list


def get_produto_tabela():
    produtos = Produto.objects.all().order_by('descricao')
    lista = [{'idproduto': itens.idproduto, 'codigo': itens.codigo, 'descricao': itens.descricao,
              'categoria': itens.categoria, 'valor': itens.valor} for itens in produtos]
    return lista


def get_tabela(id_cadastro):
    tabela = Tabela.objects.filter(idcadastro=id_cadastro)
    lista = []
    for x in tabela:
        produto = Produto.objects.get(idproduto=x.idproduto)
        lista.append({'idtabela': x.idtabela, 'codigo': produto.codigo, 'descricao': produto.descricao,
                      'categoria': produto.categoria, 'valor': x.valor})
    lista = sorted(lista, key=lambda x: x['descricao'])
    return lista


def qs_get_cliente(id_cadastro):
    pessoa = Pessoa.objects.get(idpessoa=id_cadastro)
    return pessoa
    

def qs_get_produto(id_produto):
    produto = Produto.objects.get(idproduto=id_produto)
    return produto


def qs_get_tabela(id_tabela):
    tabela = Tabela.objects.get(idtabela=id_tabela)
    return tabela


def carrega_cliente_tabela(request, id_cadastro, data):
    tabela = get_tabela(id_cadastro)
    apelido = qs_get_cliente(id_cadastro)
    contexto = context()
    contexto_tabela_selecionada = {'produtos_tabela': tabela, 'apelido': apelido}
    contexto.update(contexto_tabela_selecionada)
    data = html_tabela_selecionada(request, data, contexto)
    return data


def carrega_produto_tabela(request, data):
    contexto = context()
    contexto_tipotb = {'tipotb': 'PRODUTO'}
    contexto.update(contexto_tipotb)
    data = html_tabela_selecionada(request, data, contexto)
    return data


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


def html_tabela_selecionada(request, data, contexto):
    data['html_tabela_selecionada'] = render_to_string('tabelas/tabela_selecionada.html', contexto, request=request)
    return data


def return_json(data):
    return JsonResponse(data)


def form_tabela(request, v_form, v_idobj, v_url, v_view):
    data = dict()
    v_instance = None
    v_descricao = None
    clientes_no_tabela = None
    tipotb = None
    if request.method == 'POST':
        form = v_form
        if v_view == 'altera_valor_produto':
            v_idobj = request.POST.get('idproduto')
            if request.POST.get('tipotb') == 'PRODUTO':
                v_instance = qs_get_produto(v_idobj)
            else:
                v_instance = qs_get_tabela(v_idobj)
            form = v_form(request.POST, instance=v_instance)
            if form.is_valid():
                if form.save():
                    if request.POST.get('tipotb') == 'PRODUTO':
                        data = carrega_produto_tabela(request, data)
                    else:
                        data = carrega_cliente_tabela(request, v_instance.idcadastro, data)
        if v_view == 'nova_tabela_propria':
            v_idcadastro = request.POST.get('cliente')
            produto = get_produto_tabela()
            cadastros_tabela = []
            for x in produto:
                obj = Tabela(idcadastro = v_idcadastro, idproduto = x['idproduto'], valor = 0.00)
                cadastros_tabela.append(obj)
            Tabela.objects.bulk_create(cadastros_tabela)
            data = html_tabela_propria(request, data)
            data = carrega_cliente_tabela(request, v_idcadastro, data)
    else:
        if v_view == 'altera_valor_produto':
            if request.GET.get('tipotb') == 'PRODUTO':
                v_instance = qs_get_produto(v_idobj)
                tipotb = 'PRODUTO'
                v_descricao = v_instance.descricao
            else:
                v_instance = qs_get_tabela(v_idobj)
                tipotb = 'CLIENTE'
                produto = qs_get_produto(v_instance.idproduto)
                v_descricao = produto.descricao
        if v_view == 'nova_tabela_propria':
            clientes_no_tabela = get_cliente_no_tabela()  
            

        form = v_form(instance=v_instance)
    contexto = {'form': form, 'v_idobj': v_idobj, 'v_url': v_url, 'v_view': v_view, 'v_descricao': v_descricao,
                'tipotb': tipotb, 'clientes_no_tabela': clientes_no_tabela}
    data['html_form'] = render_to_string('tabelas/form_tabelas.html', contexto, request=request)
    return data


def form_exclui(request, v_idobj, v_view):
    data = dict()
    v_queryset = None
    v_apelido = None
    v_produto = None
    if v_view == 'delete_tabela_item':
        if request.method == 'POST':
            v_queryset = qs_get_tabela(request.POST.get('idtabela'))
            if v_queryset.delete():
                data = carrega_cliente_tabela(request, v_queryset.idcadastro, data)
        else:
            v_queryset = qs_get_tabela(v_idobj)
            v_apelido = qs_get_cliente(v_queryset.idcadastro)
            v_produto = qs_get_produto(v_queryset.idproduto)
    contexto = {'v_queryset': v_queryset, 'v_idobj': v_idobj, 'v_view': v_view, 'v_apelido': v_apelido,
               'v_produto': v_produto}
    data['html_form'] = render_to_string('tabelas/form_tabelas.html', contexto, request=request)
    return data
