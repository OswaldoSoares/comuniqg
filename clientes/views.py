from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods

from clientes import facade


@login_required
@require_GET
def index_clientes(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_pessoa = facade.obter_id(request.GET.get("id_pessoa"))
    contexto = facade.create_contexto_pessoas(
        filtro, request.GET.get("busca"), id_pessoa
    )
    if id_pessoa:
        contexto.update(facade.create_contexto_pessoa(id_pessoa))
    return render(request, "clientes/index.html", contexto)


@login_required
@require_GET
def pessoas_lista(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_pessoa = facade.obter_id(request.GET.get("id_pessoa"))
    return facade.create_data_pessoas(
        request, filtro, request.GET.get("busca", ""), id_pessoa
    )


@login_required
@require_GET
def pessoa_consulta(request):
    return facade.create_data_pessoa(
        request, facade.obter_id(request.GET.get("id_pessoa"))
    )


@login_required
@require_http_methods(["GET", "POST"])
def pessoa_form(request):
    if request.method == "POST":
        return facade.save_pessoa(request)

    modal_html = facade.modal_pessoa(request, request.GET.get("id_pessoa"))
    return JsonResponse({"modal_html": modal_html})
