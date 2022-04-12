from databaseold.models import Pessoa, Servico
from django.shortcuts import render

from .print import servico_pdf


def index_servico(request):
    servico = Servico.objects.filter(status="ENTREGAR")
    servicos = []
    for itens in servico:
        if itens.idcadastro:
            cliente = Pessoa.objects.get(idpessoa=itens.idcadastro)
            if not cliente:
                cliente = None
        servicos.append(
            {
                "idservico": itens.idservico,
                "cliente": cliente.apelido,
                "solicitante": itens.solicitante,
                "obra": itens.obra,
            }
        )
    servicos = sorted(servicos, key=lambda x: x["cliente"])
    return render(request, "servicos/index.html", {"servicos": servicos})


def print_servico(request, idservico):
    response = servico_pdf(idservico)
    return response
