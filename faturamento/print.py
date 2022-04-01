from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from comuniqg.settings import STATIC_ROOT
from io import BytesIO
from core.facade import mp, c_br
from faturamento.facade import Fatura, ItensServico, Produtos


def cabecalho(pdf, s_fatura):
    fatura = s_fatura['fatura']
    cliente = s_fatura['cliente']
    url = f'{STATIC_ROOT}/core/img/logo.png'
    v_endereco = 'RUA PE BENEDITO DE CAMARGO, 385'
    v_cidade = 'CEP 03604-010 - SÃO PAULO - SP'
    v_telefone = '(11) 2647-1200 - (11) 94233-8804 WHATSAPP - (11) 96191-8082 WHATSAPP'
    v_email = 'tecnoline@uol.com.br - comuniqg.gmail.com'
    v_pix = 'PIX: 40.062.536/0001-56'
    pdf.roundRect(mp(6), mp(6), mp(198), mp(285), 10, stroke=1, fill=0)
    pdf.drawImage(url, mp(10), mp(272), mp(55), mp(15))
    pdf.roundRect(mp(70), mp(272), mp(130), mp(15), 5)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(mp(120), mp(278), cliente.apelido)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawRightString(mp(198), mp(281), f'{fatura.idfatura}')
    pdf.drawRightString(mp(198), mp(275), c_br(fatura.valorfatura))
    pdf.setFillColor(HexColor("#c6c6c6"))
    pdf.rect(mp(6), mp(261), mp(198), mp(8), stroke=1, fill=1)
    pdf.setFillColor(HexColor("#000000"))
    pdf.setFont("Helvetica", 9)
    pdf.drawString(mp(10), mp(266), f'{v_endereco} - {v_cidade}')
    pdf.drawString(mp(10), mp(262), v_telefone)
    pdf.drawRightString(mp(200), mp(266), v_pix)
    pdf.drawRightString(mp(200), mp(262), v_email)
    return pdf


def fatura_pdf(v_fatura):
    s_fatura = Fatura(v_fatura).__dict__
    arquivo = f'Fatura {str(v_fatura).zfill(5)}.pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={arquivo}'
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    #------------------------------ Start of printing
    cabecalho(pdf, s_fatura)
    ln = 258
    servicos = s_fatura['servicos']
    for x in servicos:
        servicoitens = ItensServico(x['idservico']).__dict__['itens']
        dia = x['diaservico'].strftime("%d/%m/%Y")
        limite = (len(servicoitens) * 4) + 10
        base = ln - limite
        if base < 10:
            pagina = str(pdf.getPageNumber()).zfill(2)
            pdf.drawCentredString(mp(105), mp(11), pagina)
            pdf.showPage()
            cabecalho(pdf, s_fatura)
            ln = 258
        pdf.setFont("Helvetica-Bold", 11)
        pdf.line(mp(10), mp(ln), mp(200), mp(ln))
        ln -= 3.5
        pdf.drawString(mp(10), mp(ln), f"OS: {x['idservico']}")
        pdf.drawCentredString(mp(105), mp(ln), dia)
        pdf.drawRightString(mp(200), mp(ln), c_br(x['total']))
        ln -= 1
        pdf.line(mp(10), mp(ln), mp(200), mp(ln))
        ln -= 4
        pdf.setFont("Helvetica", 11)
        pdf.drawString(mp(10), mp(ln), 'Descrição')
        pdf.drawCentredString(mp(107), mp(ln), 'Originais')
        pdf.drawCentredString(mp(122), mp(ln), 'Cópias')
        pdf.drawCentredString(mp(140), mp(ln), 'Tamanho')
        pdf.drawRightString(mp(168), mp(ln), 'Valor')
        pdf.drawRightString(mp(200), mp(ln), 'Total')
        ln -= 4
        for y in servicoitens:
            produto = Produtos(y['idproduto']).__dict__['produto']
            valor = y['tamanho'] * y['valor']
            total = y['tamanho'] * y['valor'] * y['originais'] * y['copias']
            pdf.drawString(mp(10), mp(ln), produto.descricao)
            pdf.drawCentredString(mp(107), mp(ln), f"{y['originais']}".zfill(4))
            pdf.drawCentredString(mp(122), mp(ln), f"{y['copias']}".zfill(4))
            pdf.drawCentredString(mp(140), mp(ln), f"{y['tamanho']}")
            pdf.drawRightString(mp(168), mp(ln), c_br(valor))
            pdf.drawRightString(mp(200), mp(ln), c_br(total))
            ln -= 4
    pagina = str(pdf.getPageNumber()).zfill(2)
    pdf.drawCentredString(mp(105), mp(11), pagina)
    pdf.showPage()
    #------------------------------ End of print
    pdf.setTitle('FATURA')
    pdf.save()
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
