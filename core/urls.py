from django.urls import path
from .views import index_core

urlpatterns = [
    path('', index_core, name='index_core'),
]