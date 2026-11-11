from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import (
    require_GET,
    require_http_methods,
    require_POST,
)

from account import facade
from account.decorators import administrador_required


@administrador_required
@require_GET
def index_usuarios(request):
    """Lista de usuários e detalhes do selecionado (só administradores)."""
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_usuario = facade.obter_id(request.GET.get("id_usuario"))
    contexto = facade.create_contexto_usuarios(
        filtro, request.GET.get("busca"), id_usuario
    )
    if id_usuario:
        contexto.update(facade.create_contexto_usuario(request, id_usuario))
    return render(request, "account/usuarios.html", contexto)


@administrador_required
@require_GET
def usuarios_lista(request):
    filtro = facade.obter_filtro(request.GET.get("filtro"))
    id_usuario = facade.obter_id(request.GET.get("id_usuario"))
    return facade.create_data_usuarios(
        request, filtro, request.GET.get("busca", ""), id_usuario
    )


@administrador_required
@require_GET
def usuario_consulta(request):
    return facade.create_data_usuario(
        request, facade.obter_id(request.GET.get("id_usuario"))
    )


@administrador_required
@require_http_methods(["GET", "POST"])
def usuario_form(request):
    """GET abre o modal de novo/alterar; POST salva."""
    if request.method == "POST":
        return facade.save_usuario(request)
    modal_html = facade.modal_usuario(request, request.GET.get("id_usuario"))
    return JsonResponse({"modal_html": modal_html})


@administrador_required
@require_http_methods(["GET", "POST"])
def usuario_senha(request):
    """GET abre o modal de nova senha; POST salva."""
    if request.method == "POST":
        return facade.save_senha(request)
    id_usuario = facade.obter_id(request.GET.get("id_usuario"))
    modal_html = facade.modal_senha(request, id_usuario)
    return JsonResponse({"modal_html": modal_html})


@administrador_required
@require_POST
def usuario_situacao(request):
    return facade.alterar_situacao_usuario(request)
