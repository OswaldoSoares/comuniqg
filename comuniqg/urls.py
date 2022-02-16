"""comuniqg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path, include
from account import urls as account_urls
from clientes import urls as clientes_urls
from core import urls as core_urls
from dashboard import urls as dashboard_urls
from faturamento import urls as faturamento_urls
from produtos import urls as produtos_urls
from servicos import urls as servicos_urls
from tabelas import urls as tabelas_urls

urlpatterns = [
    path('admin/', admin.site.urls),
 #   path('account/', include(account_urls)),
 #   path('clientes/', include(clientes_urls)),
    path('dashboard/', include(dashboard_urls)),
 #   path('faturamento/', include(faturamento_urls)),
 #   path('produtos/', include(produtos_urls)),
 #   path('servicos/', include(servicos_urls)),
    path('tabelas/', include(tabelas_urls)),
    path('', include(core_urls)),
]
