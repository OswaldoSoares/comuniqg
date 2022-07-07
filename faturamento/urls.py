from django.urls import path

from .views import (
    cliente_faturada,
    index_faturamento,
    paga_fatura,
    print_fatura,
    servico_fatura,
)

urlpatterns = [
    path("", index_faturamento, name="index_faturamento"),
    path("cliente_faturada/", cliente_faturada, name="cliente_faturada"),
    path("print_fatura/<int:idfatura>", print_fatura, name="print_fatura"),
    path("servico_fatura/", servico_fatura, name="servico_fatura"),
    path("paga_fatura", paga_fatura, name="paga_fatura"),
]
