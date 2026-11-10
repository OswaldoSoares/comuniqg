from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods

from clientes import facade


@login_required
@require_GET
def index_clientes(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    contexto = facade.create_contexto_pessoas(filtro, request.GET.get("busca"))
    return render(request, "clientes/index.html", contexto)


@login_required
@require_GET
def pessoas_lista(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    return facade.create_data_pessoas(
        request, filtro, request.GET.get("busca", "")
    )


@login_required
@require_http_methods(["GET", "POST"])
def pessoa_form(request):
    if request.method == "POST":
        return facade.save_pessoa(request)

    modal_html = facade.modal_pessoa(request, request.GET.get("id_pessoa"))
    return JsonResponse({"modal_html": modal_html})
