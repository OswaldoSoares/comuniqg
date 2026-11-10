from django.db.models import Q, Value
from django.db.models.functions import Replace
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from clientes import html_data
from clientes.forms import MASCARA_ZERADA, CadastraPessoa, so_digitos
from core.tools import get_mensagem
from databaseold.models import Pessoa

FILTROS = [
    ("CLIENTE", "Clientes"),
    ("FORNECEDOR", "Fornecedores"),
    ("TODOS", "Todos"),
]
FILTRO_PADRAO = "CLIENTE"


def obter_filtro(valor):
    valor = (valor or "").upper()
    return valor if valor in dict(FILTROS) else FILTRO_PADRAO


def _sem_pontuacao(campo):
    """Documento só com dígitos, para buscar com ou sem máscara."""
    expressao = campo
    for caractere in "./-":
        expressao = Replace(expressao, Value(caractere), Value(""))
    return expressao


def get_pessoas(filtro=FILTRO_PADRAO, busca=""):
    pessoas = Pessoa.objects.all()
    if filtro != "TODOS":
        pessoas = pessoas.filter(funcao=filtro)

    busca = " ".join((busca or "").split())
    if busca:
        condicao = Q(apelido__icontains=busca) | Q(nome__icontains=busca)
        digitos = so_digitos(busca)
        if len(digitos) >= 3:
            pessoas = pessoas.annotate(
                cnpj_digitos=_sem_pontuacao("cnpj"),
                cpf_digitos=_sem_pontuacao("cpf"),
            )
            condicao |= Q(cnpj_digitos__contains=digitos) | Q(
                cpf_digitos__contains=digitos
            )
        pessoas = pessoas.filter(condicao)

    return pessoas.order_by("apelido", "idpessoa")


def documento(pessoa):
    """CNPJ ou CPF preenchido (o que não for a máscara zerada)."""
    if pessoa.cnpj and pessoa.cnpj != MASCARA_ZERADA["cnpj"]:
        return pessoa.cnpj
    if pessoa.cpf and pessoa.cpf != MASCARA_ZERADA["cpf"]:
        return pessoa.cpf
    return ""


def create_contexto_pessoas(filtro=FILTRO_PADRAO, busca=""):
    pessoas = list(get_pessoas(filtro, busca))
    for pessoa in pessoas:
        pessoa.documento = documento(pessoa)
    return {
        "pessoas": pessoas,
        "filtros": FILTROS,
        "filtro": filtro,
        "busca": busca,
        "total": len(pessoas),
    }


def create_data_pessoas(request, filtro, busca="", mensagem=None):
    """Resposta JSON com o card da lista de pessoas."""
    contexto = create_contexto_pessoas(filtro, busca)
    data = html_data.html_card_pessoas(request, contexto, {})
    data.update({"filtro": filtro, "busca": busca})
    if mensagem:
        data.update(mensagem)
    return JsonResponse(data)


def get_pessoa_or_none(id_pessoa):
    if not id_pessoa:
        return None
    return get_object_or_404(Pessoa, pk=id_pessoa)


def modal_pessoa(request, id_pessoa=None, form=None):
    pessoa = get_pessoa_or_none(id_pessoa)
    if form is None:
        form = CadastraPessoa(instance=pessoa)
    contexto = {"form": form, "pessoa": pessoa}
    return html_data.html_modal_pessoa(request, contexto)


def save_pessoa(request):
    id_pessoa = request.POST.get("id_pessoa")
    pessoa = get_pessoa_or_none(id_pessoa)
    form = CadastraPessoa(request.POST, instance=pessoa)

    if not form.is_valid():
        modal_html = modal_pessoa(request, id_pessoa, form)
        return JsonResponse({"html_form": modal_html})

    pessoa = form.save()
    codigo = "clca0002" if id_pessoa else "clca0001"
    mensagem = get_mensagem(
        codigo, funcao=pessoa.funcao, apelido=pessoa.apelido
    )
    # Mostra a lista onde a pessoa salva aparece, sem a busca anterior
    filtro = obter_filtro(request.POST.get("filtro"))
    if filtro != "TODOS":
        filtro = pessoa.funcao
    return create_data_pessoas(request, filtro, "", mensagem)
