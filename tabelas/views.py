from django.shortcuts import render

def index_tabela(request):
    contexto = {}
    return render(request, 'tabelas/index.html', contexto)
