from decimal import Decimal
import time

from django.db import connection, reset_queries

from django.shortcuts import render

from faturamento import facade
from faturamento.print import fatura_pdf


def index_faturamento(request):
    start = time.time()
    start_queries = len(connection.queries)
    mes, ano = facade.mes_ano(facade.hoje())
    contexto = facade.create_contexto_faturadas()
    contexto.update(facade.create_contexto_diario(mes, ano))
    end = time.time()
    end_queries = len(connection.queries)
    print(start_queries)
    print("tempo: %.2fs" % (end - start))
    print(end_queries)
    return render(request, "faturamento/index.html", contexto)


def cliente_faturada(request):
    v_idobj = request.GET.get("idobj")
    faturas = facade.get_cliente_faturada(v_idobj)
    contexto = facade.create_contexto_cliente_faturada(faturas, v_idobj)
    data = facade.create_data_cliente_faturada(request, contexto)
    return data


def cliente_faturar(request):
    v_idobj = request.GET.get("idobj")
    servicos = facade.get_servico_faturar(v_idobj)
    contexto = facade.create_contexto_servicos_faturar_cliente(servicos, v_idobj)
    data = facade.create_data_servico_faturar_cliente(request, contexto)
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
    mes, ano = facade.mes_ano(facade.hoje())
    contexto = facade.create_contexto_faturadas()
    contexto.update(facade.create_contexto_diario(mes, ano))
    contexto.update(facade.create_contexto_total_recebido_mes(mes, ano))
    faturas = facade.get_cliente_faturada(v_idp)
    contexto.update(facade.create_contexto_cliente_faturada(faturas, v_idp))
    data = facade.create_data_cliente_faturada(request, contexto)
    return data


def seleciona_mes_recebido(request):
    dia = request.GET.get("dia")
    meses = int(request.GET.get("periodo"))
    tipo = request.GET.get("tipo")
    nova_data = facade.altera_data(dia, 0, meses, 0)
    mes, ano = facade.mes_ano(nova_data)
    contexto = facade.create_contexto_diario(mes, ano)
    contexto.update(facade.create_contexto_total_recebido_mes(mes, ano))
    contexto.update(facade.create_contexto_pago_mes_totais(mes, ano))
    if tipo == "MENSAL":
        data = facade.create_data_mensal(request, contexto)
    if tipo == "MENSAL DETALHADO":
        data = facade.create_data_mensal_detalhado(request, contexto)
    return data


def seleciona_dia_recebido(request):
    dia = request.GET.get("dia")
    mes, ano = facade.mes_ano(dia)
    contexto = facade.create_contexto_diario(mes, ano)
    contexto.update(facade.create_contexto_total_recebido_mes(mes, ano))
    contexto.update(facade.create_contexto_pago_dia(dia))
    contexto.update(facade.create_contexto_pago_mes_totais(mes, ano))
    contexto.update({"dia": dia})
    data = facade.create_data_mensal_detalhado(request, contexto)
    return data


def seleciona_filtro_pagamento(request):
    dia = request.GET.get("dia")
    filtro = request.GET.get("filtro")
    contexto = facade.create_contexto_pago_dia_filtro(dia, filtro)
    contexto.update({"dia": dia})
    data = facade.create_data_filtro_pagamento(request, contexto)
    return data


def faturar_selecionadas(request):
    selecionadas = request.POST.getlist("selecionadas")
    if selecionadas:
        facade.faturar_os_selecionadas(selecionadas)
    v_idobj = request.POST.get("idobj")
    servicos = facade.get_servico_faturar(v_idobj)
    contexto = facade.create_contexto_faturar()
    contexto.update(facade.create_contexto_servicos_faturar_cliente(servicos, v_idobj))
    data = facade.create_data_atualiza_servico_faturado(request, contexto)
    return data
