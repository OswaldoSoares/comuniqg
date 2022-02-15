from django.shortcuts import render

def index_core(request):
    contexto = {}
    return render(request, 'core/index.html', contexto)
