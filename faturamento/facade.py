from decimal import Decimal
from django.db.models import Sum
from databaseold.models import Formapgto, Pessoa, Receber, Servico
from django.db import connection

class FaturasReceber:
    def __init__(self) -> None:
        pass
    

def context():
    faturadas = get_faturadas()
    total_faturadas = get_total_faturadas()
    total_pago = get_total_pago()
    total_recebe = total_faturadas - total_pago
    return {'faturadas': faturadas, 'total_faturadas': total_faturadas, 'total_pago': total_pago, 'total_recebe': total_recebe}


def get_faturadas():
    faturas = Receber.objects.filter(status='A RECEBER')
    lista = []
    lista_soma = []
    for itens in faturas:
        apelido = ''
        os = Servico.objects.filter(idfatura=itens.idfatura)
        if os:
            cliente = Pessoa.objects.get(idpessoa=os[0].idcadastro)
            apelido = cliente.apelido
        lista.append({'idfatura': itens.idfatura, 'valorfatura': itens.valorfatura, 'valorpago': itens.valorpago, 'apelido': apelido})
    sorted_list = sorted(lista, key=lambda x: x['apelido'])
    for itens in sorted_list:
        lista_cliente = list(filter(lambda x: x['apelido'] == itens['apelido'], sorted_list))
        soma_fatura = Decimal()
        soma_pago = Decimal()
        for x in lista_cliente:
            soma_fatura += x['valorfatura']
            soma_pago += x['valorpago']
        verifica_lista_soma = next((i for i, x in enumerate(lista_soma) if x['apelido'] == itens['apelido']), None)
        if verifica_lista_soma == None:
            lista_soma.append({'idfatura': itens['idfatura'], 'valorfatura': soma_fatura, 'valorpago': soma_pago, 'apelido': itens['apelido']})
    return lista_soma


def get_total_faturadas():
    total = Receber.objects.filter(status='A RECEBER').aggregate(total=Sum('valorfatura'))
    return total['total']


def get_total_pago():
    total = Receber.objects.filter(status='A RECEBER').aggregate(pago=Sum('valorpago'))
    return total['pago']


def get_servico_fatura():
    servico = Servico.objects.filter(status='FATURADA')
    return servico

