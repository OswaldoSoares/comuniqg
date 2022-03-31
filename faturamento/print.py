from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from comuniqg.settings import STATIC_ROOT
from io import BytesIO
from core.facade import mp, c_br
from faturamento.facade import Fatura


def cabecalho(pdf, v_fatura):
    s_fatura = Fatura(v_fatura).__dict__
    fatura = s_fatura['fatura']
    cliente = s_fatura['cliente']
    url = f'{STATIC_ROOT}/core/img/logo.png'
    v_endereco = 'RUA PE BENEDITO DE CAMARGO, 385'
    v_cidade = 'CEP 03604-010 - SÃO PAULO - SP'
    v_telefone = '(11) 2647-1200 - (11) 96191-8082 WHASTAPP'
    v_email = 'tecnoline@uol.com.br - comuniqg.gmail.com'
    v_pix = 'PIX: 00.000.000/000-00'
    pdf.roundRect(mp(6), mp(6), mp(198), mp(285), 10, stroke=1, fill=0)
    pdf.drawImage(url, mp(10), mp(272), mp(55), mp(15))
    pdf.roundRect(mp(70), mp(272), mp(130), mp(15), 5)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(mp(120), mp(278), cliente.apelido)
    pdf.drawRightString(mp(198), mp(281), f'{fatura.idfatura}')
    pdf.drawRightString(mp(198), mp(275), c_br(fatura.valorfatura))
    pdf.setFillColor(HexColor("#969696"))
    pdf.rect(mp(6), mp(261), mp(198), mp(8), stroke=1, fill=1)
    pdf.setFillColor(HexColor("#000000"))
    pdf.setFont("Helvetica", 9)
    pdf.drawString(mp(10), mp(266), f'{v_endereco} - {v_cidade}')
    pdf.drawString(mp(10), mp(262), v_telefone)
    pdf.drawRightString(mp(200), mp(266), v_pix)
    pdf.drawRightString(mp(200), mp(262), v_email)
    return pdf


def fatura_pdf(v_fatura):
    arquivo = f'Fatura {str(v_fatura).zfill(5)}.pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={arquivo}'
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    #------------------------------ Start print
    cabecalho(pdf, v_fatura)
    linha = 250.8
    
    #------------------------------ End print
    pdf.setTitle('FATURA')
    pdf.save()
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response
