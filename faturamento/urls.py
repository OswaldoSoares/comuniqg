from django.urls import path
from .views import index_faturamento, cliente_faturada

urlpatterns = [
    path('', index_faturamento, name='index_faturamento'),
    path('cliente_faturada', cliente_faturada, name='cliente_faturada'),
]