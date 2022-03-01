from django.shortcuts import render

def index_dashboard(request):
    contexto = {}
    return render(request, 'dashboard/index.html', contexto)
