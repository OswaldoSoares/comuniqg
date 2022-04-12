from decimal import Decimal

from databaseold.models import Formapgto, Pessoa, Produto, Receber, Servico, Servicoitem
from django.db import connection
from django.db.models import Sum
from django.http import JsonResponse
from django.template.loader import render_to_string


class Fatura:
    def __init__(self, v_idfatura) -> None:
        self.fatura = get_fatura(v_idfatura)
        self.servicos = get_servico(v_idfatura)
        self.cliente = get_cliente(self.servicos[0]["idpessoa"])
        self.pagamentos = get_pagamentos(v_idfatura)


class ItensServico:
    def __init__(self, v_idservico) -> None:
        self.itens = get_itens(v_idservico)


class Produtos:
    def __init__(self, v_idproduto) -> None:
        self.produto = get_produto(v_idproduto)


class ClassFatura:
    def __init__(self, v_fatura):
        self.fatura = v_fatura
        self.faturada_grouped = self.get_faturadas_grouped()

    @staticmethod
    def get_faturadas_grouped():
        faturas = Receber.objects.filter(status="A RECEBER")
        lista = []
        lista_soma = []
        for itens in faturas:
            apelido = ""
            os = Servico.objects.filter(idfatura=itens.idfatura)
            if os:
                cliente = Pessoa.objects.get(idpessoa=os[0].idcadastro)
                apelido = cliente.apelido
                idpessoa = cliente.idpessoa
            lista.append(
                {
                    "idfatura": itens.idfatura,
                    "valorfatura": itens.valorfatura,
                    "valorpago": itens.valorpago,
                    "apelido": apelido,
                    "idpessoa": idpessoa,
                }
            )

        sorted_list = sorted(lista, key=lambda x: x["apelido"])
        for itens in sorted_list:
            lista_cliente = list(
                filter(lambda x: x["apelido"] == itens["apelido"], sorted_list)
            )
            soma_fatura = Decimal()
            soma_pago = Decimal()
            for x in lista_cliente:
                soma_fatura += x["valorfatura"]
                soma_pago += x["valorpago"]
            verifica_lista_soma = next(
                (
                    i
                    for i, x in enumerate(lista_soma)
                    if x["apelido"] == itens["apelido"]
                ),
                None,
            )
            if verifica_lista_soma == None:
                lista_soma.append(
                    {
                        "apelido": itens["apelido"],
                        "valorfatura": soma_fatura,
                        "valorpago": soma_pago,
                        "idpessoa": itens["idpessoa"],
                    }
                )
        return lista_soma

    class ClassServico:
        def __init__(self, v_idfatura):
            self.servico = self.get_serv(v_idfatura)

        @staticmethod
        def get_serv(v_fatura):
            class ClassCliente:
                def __init__(self, v_idcliente):
                    self.cliente = get_apelido(v_idcliente)

            class ClassItensServico:
                def __init__(self, v_idservico):
                    self.itens = get_itens(v_idservico)

            servicos = Servico.objects.filter(idfatura=v_fatura)
            lista = [
                {
                    "idservico": itens.idservico,
                    "diaservico": itens.diaservico,
                    "total": itens.total,
                    "idpessoa": itens.idcadastro,
                    "pessoa": ClassCliente(itens.idcadastro).__dict__,
                    "itens": ClassItensServico(itens.idservico).__dict__,
                }
                for itens in servicos
            ]
            sorted_list = sorted(lista, key=lambda x: x["diaservico"])
            return sorted_list


def context():
    faturadas = get_faturadas()
    total_faturadas = get_total_faturadas()
    total_pago = get_total_pago()
    total_recebe = total_faturadas - total_pago
    return {
        "faturadas": faturadas,
        "total_faturadas": total_faturadas,
        "total_pago": total_pago,
        "total_recebe": total_recebe,
    }


def get_apelido(v_idpessoa):
    cliente = Pessoa.objects.get(idpessoa=v_idpessoa)
    return cliente.apelido


def get_cliente(v_idpessoa):
    cliente = Pessoa.objects.get(idpessoa=v_idpessoa)
    return cliente


def get_cliente_faturada(v_idpessoa):
    faturas = Receber.objects.filter(status="A RECEBER")
    lista = []
    for itens in faturas:
        os = Servico.objects.filter(idfatura=itens.idfatura, idcadastro=v_idpessoa)
        if os:
            apelido = get_apelido(v_idpessoa)
            lista.append(
                {
                    "idfatura": itens.idfatura,
                    "valorfatura": itens.valorfatura,
                    "valorpago": itens.valorpago,
                    "apelido": apelido,
                }
            )
    sorted_list = sorted(lista, key=lambda x: x["idfatura"])
    return sorted_list


def get_fatura(v_idfatura):
    fatura = Receber.objects.get(idfatura=v_idfatura)
    return fatura


def get_faturadas():
    faturas = Receber.objects.filter(status="A RECEBER")
    lista = []
    lista_soma = []
    for itens in faturas:
        apelido = ""
        os = Servico.objects.filter(idfatura=itens.idfatura)
        if os:
            cliente = Pessoa.objects.get(idpessoa=os[0].idcadastro)
            apelido = cliente.apelido
            idpessoa = cliente.idpessoa
        lista.append(
            {
                "idfatura": itens.idfatura,
                "valorfatura": itens.valorfatura,
                "valorpago": itens.valorpago,
                "apelido": apelido,
                "idpessoa": idpessoa,
            }
        )
    sorted_list = sorted(lista, key=lambda x: x["apelido"])
    for itens in sorted_list:
        lista_cliente = list(
            filter(lambda x: x["apelido"] == itens["apelido"], sorted_list)
        )
        soma_fatura = Decimal()
        soma_pago = Decimal()
        for x in lista_cliente:
            soma_fatura += x["valorfatura"]
            soma_pago += x["valorpago"]
        verifica_lista_soma = next(
            (i for i, x in enumerate(lista_soma) if x["apelido"] == itens["apelido"]),
            None,
        )
        if verifica_lista_soma == None:
            lista_soma.append(
                {
                    "apelido": itens["apelido"],
                    "valorfatura": soma_fatura,
                    "valorpago": soma_pago,
                    "idpessoa": itens["idpessoa"],
                }
            )
    return lista_soma


def get_itens(v_idservico):
    itens_os = Servicoitem.objects.filter(idservico=v_idservico)
    lista = [
        {
            "idservicoitem": itens.idservicoitem,
            "idproduto": itens.idproduto,
            "originais": itens.originais,
            "copias": itens.copias,
            "valor": itens.valor,
            "tamanho": itens.tamanho,
        }
        for itens in itens_os
    ]
    return lista


def get_pagamentos(v_idfatura):
    pgtos = Formapgto.objects.filter(fatura=v_idfatura)
    lista = [
        {
            "idformapgto": itens.idformapgto,
            "diapago": itens.diapago,
            "dinheiro": itens.dinheiro,
            "debito": itens.debito,
            "credito": itens.credito,
            "deposito": itens.deposito,
            "parcelas": itens.parcelas,
        }
        for itens in pgtos
    ]
    return lista


def get_produto(v_idproduto):
    produto = Produto.objects.get(idproduto=v_idproduto)
    return produto


def get_servico(v_fatura):
    servicos = Servico.objects.filter(idfatura=v_fatura)
    lista = [
        {
            "idservico": itens.idservico,
            "diaservico": itens.diaservico,
            "total": itens.total,
            "idpessoa": itens.idcadastro,
        }
        for itens in servicos
    ]
    sorted_list = sorted(lista, key=lambda x: x["diaservico"])
    return sorted_list


def get_servico_fatura():
    servico = Servico.objects.filter(status="FATURADA")
    return servico


def get_total_faturadas():
    total = Receber.objects.filter(status="A RECEBER").aggregate(
        total=Sum("valorfatura")
    )
    return total["total"]


def get_total_pago():
    total = Receber.objects.filter(status="A RECEBER").aggregate(pago=Sum("valorpago"))
    return total["pago"]


def html_cliente_faturada(request, v_faturas, v_idobj):
    data = dict()
    total_receber = Decimal()
    for x in v_faturas:
        total_receber += x["valorfatura"]
        total_receber -= x["valorpago"]
    apelido = get_apelido(v_idobj)
    contexto = {
        "faturas": v_faturas,
        "apelido": apelido,
        "total_receber": total_receber,
        "quantidade": len(v_faturas),
    }
    data["html_cliente_faturada"] = render_to_string(
        "faturamento/cliente_faturada.html", contexto, request=request
    )
    data = JsonResponse(data)
    return data


def html_servico_faturada(request, v_servicos, v_fatura):
    data = dict()
    contexto = {
        "servicos": v_servicos,
        "fatura": v_fatura,
        "os": len(v_servicos),
    }
    data["html_servico_faturada"] = render_to_string(
        "faturamento/servico_faturada.html", contexto, request=request
    )
    data = JsonResponse(data)
    return data
