from django.urls import path

from clientes.views import (
    index_clientes,
    pessoa_consulta,
    pessoa_form,
    pessoas_lista,
)

urlpatterns = [
    path("", index_clientes, name="index_clientes"),
    path("pessoas", pessoas_lista, name="pessoas_lista"),
    path("pessoa", pessoa_consulta, name="pessoa_consulta"),
    path("pessoa/form", pessoa_form, name="pessoa_form"),
]
