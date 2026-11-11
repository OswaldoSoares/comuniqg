from django.contrib.auth import views as auth_views
from django.urls import path

from account.forms import LoginForm
from account.views import (
    index_usuarios,
    usuario_consulta,
    usuario_form,
    usuario_senha,
    usuario_situacao,
    usuarios_lista,
)

urlpatterns = [
    path(
        "login",
        auth_views.LoginView.as_view(
            template_name="account/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("usuarios/", index_usuarios, name="index_usuarios"),
    path("usuarios/lista", usuarios_lista, name="usuarios_lista"),
    path("usuarios/consulta", usuario_consulta, name="usuario_consulta"),
    path("usuarios/form", usuario_form, name="usuario_form"),
    path("usuarios/senha", usuario_senha, name="usuario_senha"),
    path("usuarios/situacao", usuario_situacao, name="usuario_situacao"),
]
