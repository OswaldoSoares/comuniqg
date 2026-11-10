from django.db.models import Count, Max, Q, Value
from django.db.models.functions import Replace
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from clientes import html_data
from clientes.forms import CadastraPessoa, preenchido, so_digitos
from core.tools import get_mensagem
from databaseold.models import Contato, Pagar, Pessoa, Servico

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


def create_contexto_pessoas(filtro=FILTRO_PADRAO, busca="", id_pessoa=None):
    pessoas = list(get_pessoas(filtro, busca))
    return {
        "pessoas": pessoas,
        "filtros": FILTROS,
        "filtro": filtro,
        "busca": busca,
        "total": len(pessoas),
        "id_pessoa": id_pessoa,
    }


def obter_id(valor):
    """Id numérico vindo da tela, ou None."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def _dados_pessoa(pessoa):
    cidade = preenchido(pessoa.cidade)
    if cidade and preenchido(pessoa.estado):
        cidade = f"{cidade}/{pessoa.estado}"
    return [
        ("CNPJ", preenchido(pessoa.cnpj)),
        ("Inscrição estadual", preenchido(pessoa.ie)),
        ("CPF", preenchido(pessoa.cpf)),
        ("RG", preenchido(pessoa.rg)),
        ("Endereço", preenchido(pessoa.endereco)),
        ("Bairro", preenchido(pessoa.bairro)),
        ("Cidade", cidade),
        ("CEP", preenchido(pessoa.cep)),
        ("Site", preenchido(pessoa.site)),
    ]


def _contatos(id_pessoa):
    contatos = []
    for contato in Contato.objects.filter(idpessoa=id_pessoa).order_by(
        "contato", "idcontato"
    ):
        fones = [
            preenchido(fone)
            for fone in (
                contato.telefone1,
                contato.telefone2,
                contato.celular1,
                contato.celular2,
            )
        ]
        contatos.append(
            {
                "nome": preenchido(contato.contato),
                "fones": [fone for fone in fones if fone],
                "email": preenchido(contato.email),
            }
        )
    return contatos


def _movimento(pessoa):
    """Serviços do cliente ou contas a pagar do fornecedor."""
    if pessoa.funcao == "FORNECEDOR":
        totais = Pagar.objects.filter(idpessoa=pessoa.pk).aggregate(
            quantidade=Count("idpagar"), ultimo=Max("diaservico")
        )
        return {
            "rotulo": "Contas a pagar",
            "ultimo_rotulo": "Última conta",
            **totais,
        }
    totais = Servico.objects.filter(idcadastro=pessoa.pk).aggregate(
        quantidade=Count("idservico"), ultimo=Max("diaservico")
    )
    return {"rotulo": "Serviços", "ultimo_rotulo": "Último serviço", **totais}


def create_contexto_pessoa(id_pessoa):
    """Dados da pessoa selecionada para o card de detalhes."""
    pessoa = get_object_or_404(Pessoa, pk=id_pessoa)
    return {
        "pessoa": pessoa,
        "dados": _dados_pessoa(pessoa),
        "contatos": _contatos(pessoa.pk),
        "movimento": _movimento(pessoa),
    }


def create_data_pessoas(
    request, filtro, busca="", id_pessoa=None, mensagem=None
):
    """Resposta JSON com a lista e o card da pessoa selecionada.

    Sem pessoa selecionada, o card de detalhes volta vazio.
    """
    contexto = create_contexto_pessoas(filtro, busca, id_pessoa)
    data = html_data.html_card_pessoas(request, contexto, {})
    contexto_pessoa = create_contexto_pessoa(id_pessoa) if id_pessoa else {}
    data = html_data.html_card_pessoa(request, contexto_pessoa, data)
    data.update(
        {"filtro": filtro, "busca": busca, "id_pessoa": id_pessoa or ""}
    )
    if mensagem:
        data.update(mensagem)
    return JsonResponse(data)


def create_data_pessoa(request, id_pessoa):
    data = html_data.html_card_pessoa(
        request, create_contexto_pessoa(id_pessoa), {}
    )
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
    # Mostra a lista onde a pessoa salva aparece, sem a busca anterior,
    # com ela selecionada no card de detalhes
    filtro = obter_filtro(request.POST.get("filtro"))
    if filtro != "TODOS":
        filtro = pessoa.funcao
    return create_data_pessoas(request, filtro, "", pessoa.pk, mensagem)
