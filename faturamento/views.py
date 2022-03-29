from django.shortcuts import render

from faturamento.facade import context

def index_faturamento(request):
    contexto = context()
    return render(request, 'faturamento/index.html', contexto) 
