from django.db import connection

from databaseold.models import Pessoa, Servico


def create_contexto_servicos_aberta():
    aberta = Servico.objects.filter(status="ABERTA")
    servicos_aberta = []
    for itens in aberta:
        if itens.idcadastro:
            cliente = Pessoa.objects.get(idpessoa=itens.idcadastro)
            if not cliente:
                cliente = None
        servicos_aberta.append(
            {
                "idservico": itens.idservico,
                "cliente": cliente.apelido,
                "solicitante": itens.solicitante,
                "obra": itens.obra,
            }
        )
    servicos_aberta = sorted(servicos_aberta, key=lambda x: x["cliente"])
    return servicos_aberta


def create_contexto_servicos_entregar():
    entregar = Servico.objects.filter(status="ENTREGAR")
    servicos_entregar = []
    for itens in entregar:
        if itens.idcadastro:
            cliente = Pessoa.objects.get(idpessoa=itens.idcadastro)
            if not cliente:
                cliente = None
        servicos_entregar.append(
            {
                "idservico": itens.idservico,
                "cliente": cliente.apelido,
                "solicitante": itens.solicitante,
                "obra": itens.obra,
            }
        )
    servicos_entregar = sorted(servicos_entregar, key=lambda x: x["cliente"])
    return servicos_entregar
