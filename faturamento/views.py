from decimal import Decimal

from django.shortcuts import render

from faturamento import facade
from faturamento.print import fatura_pdf


def index_faturamento(request):
    mes, ano = facade.mes_ano(facade.hoje())
    contexto = facade.create_contexto_faturadas()
    contexto.update(facade.create_contexto_diario(mes, ano))
    contexto.update(facade.create_contexto_total_recebido_mes(mes, ano))
    return render(request, "faturamento/index.html", contexto)


def cliente_faturada(request):
    v_idobj = request.GET.get("idobj")
    faturas = facade.get_cliente_faturada(v_idobj)
    contexto = facade.create_contexto_cliente_faturada(faturas, v_idobj)
    data = facade.create_data_cliente_faturada(request, contexto)
    return data


def print_fatura(request, idfatura):
    response = fatura_pdf(idfatura)
    return response


def servico_fatura(request):
    v_fatura = request.GET.get("idobj")
    v_servicos = facade.get_servico(v_fatura)
    contexto = facade.create_contexto_fatura_selecionada(v_servicos, v_fatura)
    data = facade.create_data_servico_faturada(request, contexto)
    return data


def paga_fatura(request):
    v_dia = request.POST.get("dia")
    v_din = Decimal(request.POST.get("dinheiro"))
    v_deb = Decimal(request.POST.get("debito"))
    v_cre = Decimal(request.POST.get("credito"))
    # v_pix = Decimal(request.POST.get("pix"))
    v_pix = Decimal(0.00)
    v_dep = Decimal(request.POST.get("deposito"))
    v_fat = request.POST.get("idfatura")
    v_idp = int(request.POST.get("idcliente"))
    soma = v_din + v_deb + v_cre + v_pix + v_dep
    if not soma == 0.00:
        facade.paga_fatura(v_dia, v_din, v_deb, v_cre, v_pix, v_dep, v_fat)
    contexto = facade.create_contexto_faturadas()
    faturas = facade.get_cliente_faturada(v_idp)
    contexto_add = facade.create_contexto_cliente_faturada(faturas, v_idp)
    contexto.update(contexto_add)
    data = facade.create_data_cliente_faturada(request, contexto)
    return data
