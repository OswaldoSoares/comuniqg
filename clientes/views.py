from django.shortcuts import render


def index_clientes(request):
    contexto = {}
    return render(request, "clientes/index.html", contexto)
