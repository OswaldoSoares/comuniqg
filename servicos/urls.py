from django.urls import path

from .views import index_servico, print_servico

urlpatterns = [
    path("", index_servico, name="index_servico"),
    path("print_servico/<int:idservico>", print_servico, name="print_servico"),
]
