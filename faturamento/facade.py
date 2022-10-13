import datetime
from decimal import Decimal

from databaseold.models import Formapgto, Pessoa, Produto, Receber, Servico, Servicoitem
from dateutil.relativedelta import relativedelta
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


def extremos_mes(_mes, _ano):
    first_day = datetime.datetime.strptime(f"1-{int(_mes)}-{int(_ano)}", "%d-%m-%Y")
    last_day = first_day + relativedelta(months=+1, days=-1)
    return first_day, last_day


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


def get_cliente_faturar(v_idpessoa):
    faturas = Receber.objects.filter(status="A FATURAR")
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
    idpessoa = 1
    for itens in faturas:
        apelido = ""
        os = Servico.objects.filter(idfatura=itens.idfatura)
        if os:
            cliente = Pessoa.objects.get(idpessoa=os[0].idcadastro)
            apelido = cliente.apelido
            idpessoa = cliente.idpessoa
        if idpessoa == 1:
            print(itens.idfatura)
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


def get_faturar():
    os = Servico.objects.filter(status="FATURAR")
    lista = []
    lista_soma = []
    for itens in os:
        cliente = Pessoa.objects.get(idpessoa=itens.idcadastro)
        apelido = cliente.apelido
        idpessoa = cliente.idpessoa
        lista.append(
            {
                "idfatura": itens.idfatura,
                "valorfatura": itens.total,
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
        for x in lista_cliente:
            soma_fatura += x["valorfatura"]
        verifica_lista_soma = next(
            (i for i, x in enumerate(lista_soma) if x["apelido"] == itens["apelido"]),
            None,
        )
        if verifica_lista_soma == None:
            lista_soma.append(
                {
                    "apelido": itens["apelido"],
                    "valorfatura": soma_fatura,
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
            "idformapgto": i.idformapgto,
            "diapago": i.diapago,
            "dinheiro": i.dinheiro,
            "debito": i.debito,
            "credito": i.credito,
            "deposito": i.deposito,
            "parcelas": i.parcelas,
            "total": i.dinheiro + i.debito + i.credito + i.deposito,
        }
        for i in pgtos
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


def get_total_faturar():
    total = Servico.objects.filter(status="FATURAR").aggregate(total=Sum("total"))
    return total["total"]


def get_total_pago():
    total = Receber.objects.filter(status="A RECEBER").aggregate(pago=Sum("valorpago"))
    return total["pago"]


def create_contexto_cliente_faturada(v_faturas, v_idobj):
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
    return contexto


def create_contexto_pago_dia(v_dia):
    if type(v_dia) is str:
        v_dia = datetime.datetime.strptime(v_dia, "%d/%m/%Y").date()
    qs_pagamento = Formapgto.objects.filter(diapago=v_dia)
    lista_pgto = []
    total_filtro = Decimal(0.00)
    for x in qs_pagamento:
        qs_servico = Servico.objects.filter(idfatura=x.fatura)
        cliente = Pessoa.objects.get(idpessoa=qs_servico[0].idcadastro)
        lista_pgto.append(
            {
                "cliente": cliente.apelido,
                "fatura": x.fatura,
                "total": x.dinheiro + x.debito + x.credito + x.deposito,
            }
        )
        total_filtro += x.dinheiro + x.debito + x.credito + x.deposito
    lista_ordenada = sorted(lista_pgto, key=lambda d: d["cliente"])
    return {"pagamentos": lista_ordenada, "total_filtro": total_filtro}


def create_contexto_pago_mes_totais(v_dia):
    if type(v_dia) is str:
        v_dia = datetime.datetime.strptime(v_dia, "%d/%m/%Y").date()


def create_contexto_pago_mes_totais(mes, ano):
    pdm, udm = extremos_mes(mes, ano)
    qs = Formapgto.objects.filter(diapago__range=(pdm, udm)).aggregate(
        total=Sum("dinheiro")
    )
    dinheiro = qs["total"]
    qs = Formapgto.objects.filter(diapago__range=(pdm, udm)).aggregate(
        total=Sum("debito")
    )
    debito = qs["total"]
    qs = Formapgto.objects.filter(diapago__range=(pdm, udm)).aggregate(
        total=Sum("credito")
    )
    credito = qs["total"]
    qs = Formapgto.objects.filter(diapago__range=(pdm, udm)).aggregate(
        total=Sum("deposito")
    )
    deposito = qs["total"]
    contexto = {
        "dinheiro": dinheiro,
        "debito": debito,
        "credito": credito,
        "deposito": deposito,
    }
    return contexto


def create_contexto_pago_dia_filtro(v_dia, filtro):
    if type(v_dia) is str:
        v_dia = datetime.datetime.strptime(v_dia, "%d/%m/%Y").date()
    if filtro == "DINHEIRO":
        qs_pagamento = Formapgto.objects.filter(diapago=v_dia, dinheiro__gt=0.00)
    elif filtro == "DEBITO":
        qs_pagamento = Formapgto.objects.filter(diapago=v_dia, debito__gt=0.00)
    elif filtro == "CREDITO":
        qs_pagamento = Formapgto.objects.filter(diapago=v_dia, credito__gt=0.00)
    elif filtro == "DEPOSITO":
        qs_pagamento = Formapgto.objects.filter(diapago=v_dia, deposito__gt=0.00)
    else:
        qs_pagamento = Formapgto.objects.filter(diapago=v_dia)
    lista_pgto = []
    total_filtro = Decimal(0.00)
    for x in qs_pagamento:
        qs_servico = Servico.objects.filter(idfatura=x.fatura)
        cliente = Pessoa.objects.get(idpessoa=qs_servico[0].idcadastro)
        valor = Decimal(0.00)
        if filtro == "DINHEIRO":
            valor = x.dinheiro
        elif filtro == "DEBITO":
            valor = x.debito
        elif filtro == "CREDITO":
            valor = x.credito
        elif filtro == "DEPOSITO":
            valor = x.deposito
        else:
            valor = x.dinheiro + x.debito + x.credito + x.deposito
        total_filtro += valor
        lista_pgto.append(
            {
                "cliente": cliente.apelido,
                "fatura": x.fatura,
                "total": valor,
            }
        )
    lista_ordenada = sorted(lista_pgto, key=lambda d: d["cliente"])
    return {"pagamentos": lista_ordenada, "total_filtro": total_filtro}


def create_data_filtro_pagamento(request, contexto):
    data = dict()
    data = html_pgto_dia(request, contexto, data)
    return JsonResponse(data)


def create_data_cliente_faturada(request, contexto):
    data = dict()
    data = html_fatura_agrupada(request, contexto, data)
    data = html_cliente_faturada(request, contexto, data)
    data = html_mensal(request, contexto, data)
    return JsonResponse(data)


def create_data_mensal(request, contexto):
    data = dict()
    data = html_mensal(request, contexto, data)
    return JsonResponse(data)


def html_pgto_dia(request, contexto, data):
    data["html_pgto_dia"] = render_to_string(
        "faturamento/html_pagamentos_dia.html", contexto, request=request
    )
    return data


def html_mensal(request, contexto, data):
    data["html_mensal"] = render_to_string(
        "faturamento/html_recebe_mensal.html", contexto, request=request
    )
    return data


def create_data_mensal_detalhado(request, contexto):
    data = dict()
    data = html_mensal_detalhado(request, contexto, data)
    data = html_pgto_dia(request, contexto, data)
    return JsonResponse(data)


def html_mensal_detalhado(request, contexto, data):
    data["html_mensal_detalhado"] = render_to_string(
        "faturamento/html_recebe_mensal_detalhado.html", contexto, request=request
    )
    return data


def html_cliente_faturada(request, contexto, data):
    data["html_cliente_faturada"] = render_to_string(
        "faturamento/cliente_faturada.html", contexto, request=request
    )
    return data


def create_data_servico_faturada(request, contexto):
    data = dict()
    data = html_servico_faturada(request, contexto, data)
    data = html_pagamento_fatura(request, contexto, data)
    return JsonResponse(data)


def html_servico_faturada(request, contexto, data):
    data["html_servico_faturada"] = render_to_string(
        "faturamento/servico_faturada.html", contexto, request=request
    )
    return data


def html_pagamento_fatura(request, contexto, data):
    data["html_pagamento_fatura"] = render_to_string(
        "faturamento/html_pagamento_fatura.html", contexto, request=request
    )
    return data


def html_fatura_agrupada(request, contexto, data):
    data["html_fatura_agrupada"] = render_to_string(
        "faturamento/html_fatura_agrupada.html", contexto, request=request
    )
    return data


def create_data_paga_fatura(request, contexto):
    data = dict()
    data = html_fatura_agrupada(request, contexto, data)
    data = html_servico_faturada(request, contexto, data)
    data = html_pagamento_fatura(request, contexto, data)
    return data


def create_contexto_faturadas():
    faturadas = get_faturadas()
    total_faturadas = get_total_faturadas()
    total_faturar = get_total_faturar()
    total_pago = get_total_pago()
    total_recebe = total_faturadas - total_pago
    faturar = get_faturar()
    return {
        "faturadas": faturadas,
        "total_faturadas": total_faturadas,
        "total_faturar": total_faturar,
        "total_pago": total_pago,
        "total_recebe": total_recebe,
        "faturar": faturar,
    }


def create_contexto_diario(mes, ano):
    pdm, udm = extremos_mes(mes, ano)
    lista_pgto = []
    while pdm < udm + relativedelta(days=1):
        qs = Formapgto.objects.filter(diapago=pdm).aggregate(
            din=Sum("dinheiro"),
            deb=Sum("debito"),
            cre=Sum("credito"),
            dep=Sum("deposito"),
        )
        din = Decimal(0.00) if qs["din"] == None else qs["din"]
        deb = Decimal(0.00) if qs["deb"] == None else qs["deb"]
        cre = Decimal(0.00) if qs["cre"] == None else qs["cre"]
        dep = Decimal(0.00) if qs["dep"] == None else qs["dep"]
        lista_pgto.append(
            {
                "dia": pdm,
                "dinheiro": din,
                "debito": deb,
                "credito": cre,
                "deposito": dep,
                "total": din + deb + cre + dep,
            }
        )
        pdm = pdm + relativedelta(days=1)
    return {"mensal": lista_pgto, "mes": udm}


def create_contexto_total_recebido_mes(mes, ano):
    pdm, udm = extremos_mes(mes, ano)
    qs = Formapgto.objects.filter(diapago__range=(pdm, udm)).aggregate(
        din=Sum("dinheiro"),
        deb=Sum("debito"),
        cre=Sum("credito"),
        dep=Sum("deposito"),
    )
    din = Decimal(0.00) if qs["din"] == None else qs["din"]
    deb = Decimal(0.00) if qs["deb"] == None else qs["deb"]
    cre = Decimal(0.00) if qs["cre"] == None else qs["cre"]
    dep = Decimal(0.00) if qs["dep"] == None else qs["dep"]
    total = din + deb + cre + dep
    return {"total": total}


def hoje():
    hoje = datetime.datetime.today()
    return hoje


def altera_data(dia, dias, meses, anos):
    nova_data = datetime.datetime.strptime(dia, "%d/%m/%Y").date()
    nova_data = nova_data + relativedelta(days=dias, months=meses, years=anos)
    return nova_data


def mes_ano(data):
    if type(data) is str:
        data = datetime.datetime.strptime(data, "%d/%m/%Y").date()
    mes = datetime.datetime.strftime(data, "%m")
    ano = datetime.datetime.strftime(data, "%Y")
    return mes, ano


def create_contexto_fatura_selecionada(v_servicos, v_fatura):
    hoje = datetime.datetime.today()
    hoje = datetime.datetime.strftime(hoje, "%Y-%m-%d")
    pagamentos = get_pagamentos(v_fatura)
    fatura = get_fatura(v_fatura)
    total = Decimal(0.00)
    for i in pagamentos:
        total += i["total"]
    saldo = fatura.valorfatura - total
    contexto = {
        "servicos": v_servicos,
        "idpessoal": v_servicos[0]["idpessoa"],
        "fatura": v_fatura,
        "os": len(v_servicos),
        "pagamentos": pagamentos,
        "hoje": hoje,
        "saldo": saldo,
    }
    return contexto


def paga_fatura(v_dia, v_din, v_deb, v_cre, v_pix, v_dep, v_fat):
    soma = v_din + v_deb + v_cre + v_pix + v_dep
    obj = Formapgto()
    obj.fatura = v_fat
    obj.diapago = v_dia
    obj.dinheiro = v_din
    obj.debito = v_deb
    obj.credito = v_cre
    obj.deposito = v_dep
    obj.parcelas = 1
    obj.save()
    fatura = Receber.objects.get(idfatura=v_fat)
    obj = fatura
    if obj.valorpago == None:
        obj.valorpago = soma
    else:
        obj.valorpago += soma
    if obj.valorpago < obj.valorfatura:
        obj.status = obj.status
    else:
        obj.status = "RECEBIDA"
    obj.save(update_fields=["valorpago", "status"])
    servicos = Servico.objects.filter(idfatura=v_fat)
    for i in servicos:
        obj = i
        obj.status = "PAGA"
        obj.save(update_fields=["status"])
