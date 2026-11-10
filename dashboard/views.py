from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index_dashboard(request):
    contexto = {}
    return render(request, 'dashboard/index.html', contexto)
