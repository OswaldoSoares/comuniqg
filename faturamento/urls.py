from django.urls import path

from .views import (
    cliente_faturada,
    index_faturamento,
    paga_fatura,
    print_fatura,
    seleciona_dia_recebido,
    seleciona_filtro_pagamento,
    seleciona_mes_recebido,
    servico_fatura,
)

urlpatterns = [
    path(
        "",
        index_faturamento,
        name="index_faturamento",
    ),
    path(
        "cliente_faturada/",
        cliente_faturada,
        name="cliente_faturada",
    ),
    path(
        "print_fatura/<int:idfatura>",
        print_fatura,
        name="print_fatura",
    ),
    path(
        "servico_fatura/",
        servico_fatura,
        name="servico_fatura",
    ),
    path(
        "paga_fatura",
        paga_fatura,
        name="paga_fatura",
    ),
    path(
        "seleciona_mes_recebido",
        seleciona_mes_recebido,
        name="seleciona_mes_recebido",
    ),
    path(
        "seleciona_dia_recebido",
        seleciona_dia_recebido,
        name="seleciona_dia_recebido",
    ),
    path(
        "seleciona_filtro_pagamento",
        seleciona_filtro_pagamento,
        name="seleciona_filtro_pagamento",
    ),
]
