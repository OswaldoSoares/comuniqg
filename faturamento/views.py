from decimal import Decimal

from django.shortcuts import render

from faturamento import facade
from faturamento.print import fatura_pdf


def cliente_faturada(request):
    v_idobj = request.GET.get("idobj")
    faturas = facade.get_cliente_faturada(v_idobj)
    data = facade.html_cliente_faturada(request, faturas, v_idobj)
    return data


def index_faturamento(request):
    contexto = facade.context()
    return render(request, "faturamento/index.html", contexto)


def print_fatura(request, idfatura):
    response = fatura_pdf(idfatura)
    return response


def servico_fatura(request):
    v_idobj = request.GET.get("idobj")
    servicos = facade.get_servico(v_idobj)
    data = facade.html_servico_faturada(request, servicos, v_idobj)
    return data


def paga_fatura(request):
    print(request.POST)
    v_dia = request.POST.get("dia")
    v_din = Decimal(request.POST.get("dinheiro"))
    v_deb = Decimal(request.POST.get("debito"))
    v_cre = Decimal(request.POST.get("credito"))
    # v_pix = Decimal(request.POST.get("pix"))
    v_pix = Decimal(0.00)
    v_dep = Decimal(request.POST.get("deposito"))
    v_fat = request.POST.get("idfatura")
    soma = v_din + v_deb + v_cre + v_pix + v_dep
    if not soma == 0.00:
        facade.paga_fatura(v_dia, v_din, v_deb, v_cre, v_pix, v_dep, v_fat)
