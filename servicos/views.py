from databaseold.models import Pessoa, Servico
from django.shortcuts import render

from .print import servico_pdf


def index_servico(request):
    servico = Servico.objects.filter(status="ENTREGAR")
    os = {}
    for item in servico:
        os[item.idservico] = {}
        cliente_queryset = Pessoa.objects.filter(idpessoa=item.idcadastro)
        cliente = None
        if cliente_queryset:
            cliente = list(cliente_queryset.values_list("apelido").values())[0]
        nome = None
        if cliente:
            nome = cliente.get("apelido")
        os[item.idservico]["idservico"] = item.idservico
        os[item.idservico]["Cliente"] = nome
        os[item.idservico]["Solicitante"] = item.solicitante
        os[item.idservico]["Obra"] = item.obra
        os[item.idservico]["Itens"] = {}
        # itens_servico_queryset = Servicoitem.objects.filter(idservico=item.idservico)
        # itens_servico = list(itens_servico_queryset.values_list().values())
        # for x in itens_servico:
        #     os[x.idservicoitem]['Originais'] = 1
        #     os[x.idservicoitem]['Copias'] = 2
        #     os[x.idservicoitem]['Valor'] = 3
        #     os[x.idservicoitem]['Tmanho'] = 4

    return render(request, "servicos/index.html", {"os": os})


def print_servico(request, idservico):
    print(idservico)
    response = servico_pdf(idservico)
    return response
