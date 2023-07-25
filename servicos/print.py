from io import BytesIO

from comuniqg.settings import STATIC_ROOT
from core.facade import mp
from databaseold.models import Pessoa, Produto, Servico, Servicoitem
from django.http import HttpResponse
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


def servico_pdf(idservico):
    """
    Função que gera o PDF da OS. Impressão em uma folha A4 em posição landscape, imprime 2 vias na mesma folha,
    a variável posx que possibilita a impressão da 2 via ao lado. Utilização da biblioteca ReportLab.
    :param request: request
    :param idservico: integer
    :return:
    """
    url = f"{STATIC_ROOT}/core/img/logo.png"
    v_endereco = "RUA NUNES DE SIQUEIRA, 26"
    v_cidade = "CEP 03604-050 - SÃO PAULO - SP"
    v_telefone = "(11) 2647-1200 - (11) 94233-8804 WHATSAPP - (11) 99777-2837 WHATSAPP"
    v_email = "tecnoline@uol.com.br - comuniqg@uol.com.br"
    v_pix = "PIX: 40.062.536/0001-56"
    servico = Servico.objects.get(idservico=idservico)
    cliente = Pessoa.objects.get(idpessoa=servico.idcadastro)
    qs_servico_item = Servicoitem.objects.filter(idservico=idservico)
    servico_item = list(qs_servico_item.values())
    for index, item in enumerate(servico_item):
        idproduto = servico_item[index]["idproduto"]
        produto = Produto.objects.get(idproduto=idproduto)
        servico_item[index]["idproduto"] = produto.descricao
        servico_item[index]["codigo"] = produto.codigo
    response = HttpResponse(content_type="application/pdf")
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    posx = 0
    for n in range(2):
        pdf.roundRect(mp(5 + posx), mp(5), mp(138.5), mp(200), 10)
        pdf.drawImage(url, mp(11 + posx), mp(188), mp(55.21), mp(15))
        pdf.roundRect(mp(101 + posx), mp(190), mp(30), mp(10), 10)
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(mp(106.5 + posx), mp(193.5), "OS: " + str(servico.idservico))
        pdf.setFont("Times-Bold", 10)
        pdf.drawCentredString(mp(74 + posx), mp(184), f"{v_endereco} - {v_cidade}")
        pdf.drawCentredString(mp(74 + posx), mp(180), v_telefone)
        pdf.drawCentredString(mp(74 + posx), mp(176), v_email)
        pdf.line(mp(5 + posx), mp(175), mp(143.5 + posx), mp(175))
        pdf.line(mp(5 + posx), mp(165), mp(143.5 + posx), mp(165))
        pdf.setFont("Times-Bold", 10)
        pdf.setFillColor(HexColor("#c1c1c1"))
        pdf.setStrokeColor(HexColor("#c1c1c1"))
        pdf.rect(mp(5.5 + posx), mp(170), mp(67.75), mp(4.5), fill=1, stroke=1)
        pdf.rect(mp(74.5 + posx), mp(170), mp(68.25), mp(4.5), fill=1, stroke=1)
        pdf.setFillColor(HexColor("#000000"))
        pdf.setStrokeColor(HexColor("#000000"))
        pdf.drawCentredString(mp(39.5 + posx), mp(171), cliente.apelido)
        pdf.drawCentredString(mp(108.5 + posx), mp(171), servico.solicitante)
        pdf.setFont("Times-Roman", 9)
        pdf.drawString(mp(24 + posx), mp(166), "Descrição")
        # pdf.drawCentredString(mp(50.5), mp(166), 'Código')
        pdf.drawRightString(mp(73 + posx), mp(166), "Originais")
        pdf.drawRightString(mp(85 + posx), mp(166), "Cópias")
        pdf.drawRightString(mp(96 + posx), mp(166), "Medida")
        pdf.drawRightString(mp(107 + posx), mp(166), "Quant.")
        pdf.drawRightString(mp(120 + posx), mp(166), "Valor")
        pdf.drawRightString(mp(138 + posx), mp(166), "Total")
        linha = 166
        total = 0
        for x in servico_item:
            pdf.drawString(mp(6 + posx), mp(linha - 4), x.get("idproduto"))
            # pdf.drawCentredString(mp(50.5), mp(linha-4), x.get('codigo'))
            pdf.drawRightString(mp(69 + posx), mp(linha - 4), str(x.get("originais")))
            pdf.drawRightString(mp(83 + posx), mp(linha - 4), str(x.get("copias")))
            pdf.drawRightString(mp(95 + posx), mp(linha - 4), str(x.get("tamanho")))
            pdf.drawRightString(
                mp(104 + posx), mp(linha - 4), str(x.get("originais") * x.get("copias"))
            )
            pdf.drawRightString(
                mp(123 + posx),
                mp(linha - 4),
                "R$ {:.2f}".format(x.get("valor")).replace(".", ","),
            )
            pdf.drawRightString(
                mp(142 + posx),
                mp(linha - 4),
                "R$ {:.2f}".format(
                    x.get("originais")
                    * x.get("copias")
                    * x.get("tamanho")
                    * x.get("valor")
                ).replace(".", ","),
            )
            total += (
                x.get("originais") * x.get("copias") * x.get("tamanho") * x.get("valor")
            )
            pdf.line(mp(5 + posx), mp(linha - 5), mp(143.5 + posx), mp(linha - 5))
            linha -= 4
        pdf.setFillColor(HexColor("#c1c1c1"))
        pdf.setStrokeColor(HexColor("#c1c1c1"))
        pdf.rect(mp(5.5 + posx), mp(linha - 7.5), mp(137.5), mp(6), fill=1, stroke=1)
        pdf.setFillColor(HexColor("#000000"))
        pdf.setStrokeColor(HexColor("#000000"))
        pdf.setFont("Times-Bold", 10)
        pdf.drawString(
            mp(6 + posx), mp(linha - 6), "Data: {:%d/%m/%Y}".format(servico.diaservico)
        )
        pdf.drawRightString(
            mp(142 + posx), mp(linha - 6), "R$ {:.2f}".format(total).replace(".", ",")
        )
        pdf.line(mp(5 + posx), mp(linha - 8), mp(143.5 + posx), mp(linha - 8))
        pdf.line(mp(5 + posx), mp(55), mp(143.5 + posx), mp(55))
        pdf.drawString(mp(7 + posx), mp(51), "Observações:")
        obs_style = ParagraphStyle(
            "claro",
            fontName="Times-Roman",
            fontSize=8,
            leading=8,
            alignment=TA_JUSTIFY,
        )
        if servico.obs:
            v_paragraph = Paragraph(servico.obs, style=obs_style)
            v_paragraph.wrapOn(pdf, mp(130), mp(19))
            v_height = (v_paragraph.height / 8) * 3
            v_paragraph.drawOn(pdf, mp(8 + posx), mp(49 - v_height))
        pdf.rect(mp(7 + posx), mp(34), mp(134.5), mp(15))
        pdf.drawString(mp(7 + posx), mp(29), "Obra")
        pdf.drawString(mp(7 + posx), mp(24), servico.obra)
        pdf.drawString(
            mp(7 + posx),
            mp(16),
            "Recebemos os originais e as cópias em perfeito estado.",
        )
        pdf.drawString(mp(7 + posx), mp(7), "Name:________________________________")
        pdf.drawString(mp(75 + posx), mp(7), "ASS:________________________________")
        posx += 148.5
    pdf.setTitle("OS" + str(servico.idservico) + ".pdf")
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
