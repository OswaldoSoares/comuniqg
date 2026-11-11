// Funções comuns às telas de cadastro no padrão ui-* (ui-cadastro.css):
// ajax, sessão expirada e o modal #MyModal com formulário.

// Como executarAjax (ajax.js), mas sem voltar ao topo da página,
// para não perder a posição na lista
function uiAjax(url, type, data, sucessoCallback) {
    $.ajax({
        type: type,
        url: url,
        data: data,
        beforeSend: function() {
            $(".box-loader").show();
        },
        success: function(response) {
            $(".box-loader").hide();
            sucessoCallback(response);
        },
        error: function(error) {
            console.log("ERROR: ", error);
            $(".box-loader").hide();
            mostrarToast("Não foi possível concluir a operação.", "error");
        }
    });
}

// Sessão expirada: o Django devolve a tela de login (HTML) em vez do JSON.
// Recarregar a página leva ao login e, depois dele, de volta para cá.
function uiSessaoExpirada(data) {
    if (typeof data !== "object") {
        window.location.reload();
        return true;
    }
    return false;
}

// Foca o primeiro campo com erro ou, se não houver erro, o primeiro campo
function uiFocaCampo(modal) {
    var form = modal.find(".modal-body form");
    var campos = form.find(".errorlist").first().closest(".ui-campo").find("input, select, textarea");
    if (!campos.length) {
        campos = form.find("input:visible, select:visible");
    }
    campos.first().trigger("focus");
}

// Liga o formulário do modal: aoCarregar (máscaras etc.), botão salvar e
// envio por ajax. Com erro, o servidor devolve html_form e o formulário é
// trocado; sem erro, o modal fecha e aoSalvar recebe a resposta.
// opcoes: {aoCarregar(modal), dadosExtras() -> objeto, aoSalvar(data)}
function uiModalForm(modal, opcoes) {
    var form = modal.find(".modal-body form");
    if (opcoes.aoCarregar) {
        opcoes.aoCarregar(modal);
    }
    modal.find(".modal-footer .btn-save").off("click").on("click", function() {
        form.trigger("submit");
    });
    form.on("submit", function(event) {
        event.preventDefault();
        var dados = form.serialize();
        if (opcoes.dadosExtras) {
            dados += "&" + $.param(opcoes.dadosExtras());
        }
        uiAjax(form.attr("action"), "POST", dados, function(data) {
            if (uiSessaoExpirada(data)) {
                return;
            }
            if (data["html_form"]) {
                modal.find(".modal-body").html(data["html_form"]);
                uiModalForm(modal, opcoes);
                uiFocaCampo(modal);
            } else {
                modal.modal("hide");
                opcoes.aoSalvar(data);
            }
        });
    });
}

// Abre o #MyModal no visual ui (classe modal-ui enquanto aberto), com
// ícone no título e no botão salvar. As outras telas trocam título e
// botão com .text(), o que apaga os ícones.
// opcoes: {titulo, icone, html, aoCarregar, dadosExtras, aoSalvar}
function uiModalAbre(opcoes) {
    var modal = $("#MyModal");
    modal.find(".modal-title").empty().append(
        $("<i>").addClass("bi " + opcoes.icone),
        $("<span>").text(opcoes.titulo)
    );
    modal.find(".modal-footer .btn-save").empty().append(
        $("<i>").addClass("bi bi-check-lg"),
        $("<span>").text("SALVAR")
    );
    modal.find(".modal-body").html(opcoes.html);
    uiModalForm(modal, opcoes);
    // O Bootstrap foca o próprio modal ao terminar de abrir,
    // então o foco no campo só pode ser dado depois disso
    modal.off("shown.bs.modal.ui").one("shown.bs.modal.ui", function() {
        uiFocaCampo(modal);
    });
    modal.addClass("modal-ui");
    modal.off("hidden.bs.modal.ui").one("hidden.bs.modal.ui", function() {
        modal.removeClass("modal-ui");
    });
    modal.modal("show");
    return modal;
}
