from django.template.loader import render_to_string


def html_card_pessoas(request, contexto, data):
    data["html-card-pessoas"] = render_to_string(
        "clientes/components/pessoas.html", contexto, request=request
    )
    return data


def html_modal_pessoa(request, contexto):
    return render_to_string(
        "clientes/modal_pessoa.html", contexto, request=request
    )
