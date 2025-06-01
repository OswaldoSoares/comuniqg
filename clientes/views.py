from django.shortcuts import render


def index_clientes():
    contexto = {}
    return render("/cliente/index.html", contexto)
