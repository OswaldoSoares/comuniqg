from django.urls import path
from clientes.views import index_clientes

urlpatterns = [
    path("index_clientes", index_clientes, name="index_clientes",),
]
