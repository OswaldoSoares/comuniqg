from databaseold.models import Receber

def context():
    faturadas = get_faturadas()
    return {'faturadas': faturadas}


def get_faturadas():
    faturas = Receber.objects.filter(status='A RECEBER')
    lista = [{'idfatura': itens.idfatura, 'diafatura': itens.diafatura, 'valorfatura': itens.valorfatura, 'valorpago': itens.valorpago} for itens in faturas]
    return lista
