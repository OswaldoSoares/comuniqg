from django.urls import path
from .views import index_faturamento, cliente_faturada, print_fatura, servico_fatura

urlpatterns = [
    path('', index_faturamento, name='index_faturamento'),
    path('cliente_faturada/', cliente_faturada, name='cliente_faturada'),
    path('print_fatura/', print_fatura, name='print_fatura'),
    path('servico_fatura/', servico_fatura, name='servico_fatura'),
]