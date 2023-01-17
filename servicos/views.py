from django.shortcuts import render

from servicos import facade

from .print import servico_pdf


def index_servico(request):
    aberta = facade.create_contexto_servicos_aberta()
    entregar = facade.create_contexto_servicos_entregar()
    return render(
        request, "servicos/index.html", {"servicos": entregar, "aberta": aberta}
    )


def print_servico(request, idservico):
    response = servico_pdf(idservico)
    return response
