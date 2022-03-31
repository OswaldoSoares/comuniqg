from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO
from core.facade import mp


def cabecalho(pdf, v_fatura):
    pdf.roundRect(mp(10), mp(10), mp(190), mp(277), 10)
    return pdf


def fatura_pdf(v_fatura):
    arquivo = 'Fatura.pdf'
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
