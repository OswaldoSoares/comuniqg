from django.shortcuts import render
from faturamento.facade import context, get_apelido, get_cliente_faturada, html_cliente_faturada


def index_faturamento(request):
    contexto = context()
    return render(request, 'faturamento/index.html', contexto) 


def cliente_faturada(request):
    v_idobj = request.GET.get('idobj')
    faturas = get_cliente_faturada(v_idobj)
    apelido = get_apelido(v_idobj)
    contexto = {'faturas': faturas, 'apelido': apelido}
    data = html_cliente_faturada(request, contexto)
    return data