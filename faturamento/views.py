from django.shortcuts import render
from faturamento.facade import context, get_cliente_faturada, get_servico, html_cliente_faturada, html_servico_faturada


def index_faturamento(request):
    contexto = context()
    return render(request, 'faturamento/index.html', contexto) 


def cliente_faturada(request):
    v_idobj = request.GET.get('idobj')
    faturas = get_cliente_faturada(v_idobj)
    data = html_cliente_faturada(request, faturas, v_idobj)
    return data


def print_fatura(request):
    v_idobj = request.GET.get('idobj')


def servico_fatura(request):
    v_idobj = request.GET.get('idobj')
    servicos = get_servico(v_idobj)
    data = html_servico_faturada(request, servicos)
    return data