from django.urls import path
from .views import index_faturamento

urlpatterns = [
    path('', index_faturamento, name='index_faturamento')
]