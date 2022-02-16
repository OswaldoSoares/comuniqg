from django.shortcuts import render

from comuniqg.development import DATABASES

def index_dashboard(request):
    contexto = {'databases': DATABASES}
    return render(request, 'dashboard/index.html', contexto)
