from django.shortcuts import render

from faturamento.facade import (
    context,
    get_cliente_faturada,
    get_servico,
    html_cliente_faturada,
    html_servico_faturada,
)
from faturamento.print import fatura_pdf


def cliente_faturada(request):
    v_idobj = request.GET.get("idobj")
    faturas = get_cliente_faturada(v_idobj)
    data = html_cliente_faturada(request, faturas, v_idobj)
    return data


def index_faturamento(request):
    contexto = context()
    return render(request, "faturamento/index.html", contexto)


def print_fatura(request, idfatura):
    response = fatura_pdf(idfatura)
    return response


def servico_fatura(request):
    v_idobj = request.GET.get("idobj")
    servicos = get_servico(v_idobj)
    data = html_servico_faturada(request, servicos, v_idobj)
    return data
