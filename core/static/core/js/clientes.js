// Cadastro de clientes e fornecedores (clientes/index.html)

// Sessão expirada: o Django devolve a tela de login (HTML) em vez do JSON.
// Recarregar a página leva ao login e, depois dele, de volta para cá.
function pessoasSessaoExpirada(data) {
    if (typeof data !== "object") {
        window.location.reload();
        return true;
    }
    return false;
}

function pessoasFiltro() {
    return $(".js-pessoas").attr("data-filtro") || "";
}

function pessoasMarcaFiltro(filtro) {
    $(".js-pessoas").attr("data-filtro", filtro);
    $(".js-pessoa-filtro").each(function() {
        var ativo = $(this).data("filtro") === filtro;
        $(this).toggleClass("pessoas-filtro-ativo", ativo);
        $(this).attr("aria-pressed", ativo ? "true" : "false");
    });
}

function pessoasAtualiza(data) {
    $(".card-pessoas-lista").html(data["html-card-pessoas"]);
    if (data["filtro"]) {
        pessoasMarcaFiltro(data["filtro"]);
    }
    if (typeof data["busca"] === "string" && $(".js-pessoa-busca").val() !== data["busca"]) {
        $(".js-pessoa-busca").val(data["busca"]);
    }
    if (data["mensagem"]) {
        mostrarToast(data["mensagem"], data["tipo"]);
    }
}

// Lista: filtro e busca sem o loader de tela cheia, para não piscar
// a cada tecla; só a resposta da última busca é usada.
var pessoasRequisicao = 0;

function pessoasCarrega() {
    var numero = ++pessoasRequisicao;
    $.ajax({
        type: "GET",
        url: $(".js-pessoas").data("url-lista"),
        data: {filtro: pessoasFiltro(), busca: $(".js-pessoa-busca").val()},
        success: function(data) {
            if (numero !== pessoasRequisicao || pessoasSessaoExpirada(data)) {
                return;
            }
            pessoasAtualiza(data);
        },
        error: function(error) {
            console.log("ERROR: ", error);
        }
    });
}

$(document).on("click", ".js-pessoa-filtro", function() {
    pessoasMarcaFiltro($(this).data("filtro"));
    pessoasCarrega();
});

var pessoasEspera = null;

$(document).on("input", ".js-pessoa-busca", function() {
    clearTimeout(pessoasEspera);
    pessoasEspera = setTimeout(pessoasCarrega, 350);
});

// Modal de novo e alterar

function pessoaMascaras(modal) {
    modal.find("[data-mascara]").each(function() {
        $(this).mask($(this).data("mascara"));
    });
}

// Foca o primeiro campo com erro ou, se não houver erro, o primeiro campo
function pessoaFocaCampo(modal) {
    var form = modal.find(".modal-body form");
    var campos = form.find(".errorlist").first().closest(".pessoa-campo").find("input, select, textarea");
    if (!campos.length) {
        campos = form.find("input:visible, select:visible");
    }
    campos.first().trigger("focus");
}

function pessoaSubmit(modal) {
    var form = modal.find(".modal-body form");
    pessoaMascaras(modal);
    modal.find(".modal-footer .btn-save").off("click").on("click", function() {
        form.trigger("submit");
    });
    form.on("submit", function(event) {
        event.preventDefault();
        var dados = form.serialize() + "&" + $.param({filtro: pessoasFiltro()});
        executarAjax(form.attr("action"), "POST", dados, function(data) {
            if (pessoasSessaoExpirada(data)) {
                return;
            }
            if (data["html_form"]) {
                modal.find(".modal-body").html(data["html_form"]);
                pessoaSubmit(modal);
                pessoaFocaCampo(modal);
            } else {
                modal.modal("hide");
                pessoasAtualiza(data);
            }
        });
    });
}

$(document).on("click", ".js-pessoa-abrir", function() {
    var botao = $(this);
    var modal = $("#MyModal");
    var requestData = {};
    if (botao.data("id_pessoa")) {
        requestData["id_pessoa"] = botao.data("id_pessoa");
    }
    executarAjax(botao.data("url"), "GET", requestData, function(data) {
        if (pessoasSessaoExpirada(data)) {
            return;
        }
        modal.find(".modal-title").text(botao.data("title"));
        modal.find(".modal-footer .btn-save").text("SALVAR");
        modal.find(".modal-body").html(data["modal_html"]);
        pessoaSubmit(modal);
        // O Bootstrap foca o próprio modal ao terminar de abrir,
        // então o foco no campo só pode ser dado depois disso
        modal.off("shown.bs.modal.pessoa").one("shown.bs.modal.pessoa", function() {
            pessoaFocaCampo(modal);
        });
        modal.modal("show");
    });
});
