from databaseold.models import Tabela, Pessoa

def context():
    clientes = get_clientes()
    clientes_tabela = get_cliente_tabela()
    context = {'clientes': clientes, 'clientes_tabela': clientes_tabela}
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
