from django.urls import path
from .views import index_dashboard

urlpatterns = [
    path('', index_dashboard, name='index_dashboard')
]