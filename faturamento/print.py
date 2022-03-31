from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO


def cabecalho(pdf, fatura):
    pass


def fatura_pdf(fatura):
    arquivo = 'Fatura.pdf'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={arquivo}'
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)


    pdf.drawString(12 , 12, 'TESTE')

    pdf.setTitle('FATURA')
    pdf.save()
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response
