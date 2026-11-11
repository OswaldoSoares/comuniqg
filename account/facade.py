from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from account import html_data
from account.forms import NovoUsuarioForm, SenhaUsuarioForm, UsuarioForm
from account.models import Account
from core.tools import get_mensagem

FILTROS = [
    ("ATIVOS", "Ativos"),
    ("INATIVOS", "Inativos"),
    ("TODOS", "Todos"),
]
FILTRO_PADRAO = "ATIVOS"


def obter_filtro(valor):
    valor = (valor or "").upper()
    return valor if valor in dict(FILTROS) else FILTRO_PADRAO


def obter_id(valor):
    """Id numérico vindo da tela, ou None."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def get_usuarios(filtro=FILTRO_PADRAO, busca=""):
    usuarios = Account.objects.all()
    if filtro == "ATIVOS":
        usuarios = usuarios.filter(is_active=True)
    elif filtro == "INATIVOS":
        usuarios = usuarios.filter(is_active=False)

    busca = " ".join((busca or "").split())
    if busca:
        usuarios = usuarios.filter(
            Q(first_name__icontains=busca)
            | Q(last_name__icontains=busca)
            | Q(email__icontains=busca)
        )
    return usuarios.order_by("first_name", "last_name", "email")


def create_contexto_usuarios(filtro=FILTRO_PADRAO, busca="", id_usuario=None):
    usuarios = list(get_usuarios(filtro, busca))
    return {
        "usuarios": usuarios,
        "filtros": FILTROS,
        "filtro": filtro,
        "busca": busca,
        "total": len(usuarios),
        "id_usuario": id_usuario,
    }


def create_contexto_usuario(request, id_usuario):
    """Usuário selecionado para o card de detalhes."""
    usuario = get_object_or_404(Account, pk=id_usuario)
    return {"usuario": usuario, "eu": usuario.pk == request.user.pk}


def create_data_usuarios(
    request, filtro, busca="", id_usuario=None, mensagem=None
):
    """Resposta JSON com a lista e o card do usuário selecionado.

    Sem usuário selecionado, o card de detalhes volta vazio.
    """
    contexto = create_contexto_usuarios(filtro, busca, id_usuario)
    data = html_data.html_card_usuarios(request, contexto, {})
    contexto_usuario = (
        create_contexto_usuario(request, id_usuario) if id_usuario else {}
    )
    data = html_data.html_card_usuario(request, contexto_usuario, data)
    data.update(
        {"filtro": filtro, "busca": busca, "id_usuario": id_usuario or ""}
    )
    if mensagem:
        data.update(mensagem)
    return JsonResponse(data)


def create_data_usuario(request, id_usuario):
    data = html_data.html_card_usuario(
        request, create_contexto_usuario(request, id_usuario), {}
    )
    return JsonResponse(data)


def get_usuario_or_none(id_usuario):
    if not id_usuario:
        return None
    return get_object_or_404(Account, pk=id_usuario)


def _form_usuario(request, usuario, dados=None):
    """Novo usuário (com senha) ou alteração (sem senha)."""
    if usuario is None:
        return NovoUsuarioForm(dados)
    return UsuarioForm(dados, instance=usuario, editor=request.user)


def modal_usuario(request, id_usuario=None, form=None):
    usuario = get_usuario_or_none(id_usuario)
    if form is None:
        form = _form_usuario(request, usuario)
    contexto = {"form": form, "usuario": usuario}
    return html_data.html_modal_usuario(request, contexto)


def _resposta_lista(request, usuario, mensagem):
    """Lista com o usuário salvo selecionado, sem a busca anterior.

    Se o filtro atual esconderia o usuário, mostra todos.
    """
    filtro = obter_filtro(request.POST.get("filtro"))
    if (filtro == "ATIVOS" and not usuario.is_active) or (
        filtro == "INATIVOS" and usuario.is_active
    ):
        filtro = "TODOS"
    return create_data_usuarios(request, filtro, "", usuario.pk, mensagem)


def save_usuario(request):
    id_usuario = request.POST.get("id_usuario")
    usuario = get_usuario_or_none(id_usuario)
    form = _form_usuario(request, usuario, request.POST)

    if not form.is_valid():
        modal_html = modal_usuario(request, id_usuario, form)
        return JsonResponse({"html_form": modal_html})

    usuario = form.save()
    codigo = "acus0002" if id_usuario else "acus0001"
    mensagem = get_mensagem(codigo, email=usuario.email)
    return _resposta_lista(request, usuario, mensagem)


def modal_senha(request, id_usuario, form=None):
    usuario = get_object_or_404(Account, pk=id_usuario)
    if form is None:
        form = SenhaUsuarioForm(usuario)
    contexto = {"form": form, "usuario": usuario}
    return html_data.html_modal_senha(request, contexto)


def save_senha(request):
    """Nova senha definida pelo administrador."""
    usuario = get_object_or_404(Account, pk=request.POST.get("id_usuario"))
    form = SenhaUsuarioForm(usuario, request.POST)
    if not form.is_valid():
        modal_html = modal_senha(request, usuario.pk, form)
        return JsonResponse({"html_form": modal_html})

    form.save()
    if usuario.pk == request.user.pk:
        # Trocar a própria senha encerraria a sessão
        update_session_auth_hash(request, usuario)
    mensagem = get_mensagem("acus0003", email=usuario.email)
    return _resposta_lista(request, usuario, mensagem)


def alterar_situacao_usuario(request):
    """Ativa ou inativa; ninguém inativa o próprio usuário."""
    usuario = get_object_or_404(Account, pk=request.POST.get("id_usuario"))
    if usuario.pk == request.user.pk:
        return _resposta_lista(request, usuario, get_mensagem("acus0006"))

    usuario.is_active = not usuario.is_active
    usuario.save(update_fields=["is_active"])
    codigo = "acus0004" if usuario.is_active else "acus0005"
    mensagem = get_mensagem(codigo, email=usuario.email)
    return _resposta_lista(request, usuario, mensagem)
