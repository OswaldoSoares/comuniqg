from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index_clientes(request):
    contexto = {}
    return render(request, "clientes/index.html", contexto)
