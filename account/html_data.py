from django.template.loader import render_to_string


def html_card_usuarios(request, contexto, data):
    data["html-card-usuarios"] = render_to_string(
        "account/components/usuarios.html", contexto, request=request
    )
    return data


def html_card_usuario(request, contexto, data):
    data["html-card-usuario"] = render_to_string(
        "account/components/usuario.html", contexto, request=request
    )
    return data


def html_modal_usuario(request, contexto):
    return render_to_string(
        "account/modal_usuario.html", contexto, request=request
    )


def html_modal_senha(request, contexto):
    return render_to_string(
        "account/modal_senha.html", contexto, request=request
    )
