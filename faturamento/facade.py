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
    servico = get_servico_fatura()
    lista = []
    for itens in faturas:
        apelido = ' '
        os = servico.filter(idfatura=itens.idfatura)
        if os:
            cliente = Pessoa.objects.get(idpessoa=os[0].idcadastro)
            apelido = cliente.apelido
        lista.append({'idfatura': itens.idfatura, 'diafatura': itens.diafatura, 'valorfatura': itens.valorfatura, 'valorpago': itens.valorpago, 'apelido': apelido})
    return lista


def get_total_faturadas():
    total = Receber.objects.filter(status='A RECEBER').aggregate(total=Sum('valorfatura'))
    return total['total']


def get_total_pago():
    total = Receber.objects.filter(status='A RECEBER').aggregate(pago=Sum('valorpago'))
    return total['pago']


def get_servico_fatura():
    servico = Servico.objects.filter(status='FATURADA')
    return servico

