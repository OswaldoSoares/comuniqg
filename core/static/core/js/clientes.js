// Cadastro de clientes e fornecedores (clientes/index.html)

// Como executarAjax (ajax.js), mas sem voltar ao topo da página,
// para não perder a posição na lista ao abrir um cadastro
function pessoasAjax(url, type, data, sucessoCallback) {
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

// Pessoa aberta no card de detalhes
function pessoasSelecionada() {
    return $(".js-pessoas").attr("data-id_pessoa") || "";
}

function pessoasAtualiza(data) {
    if (data["html-card-pessoas"]) {
        $(".card-pessoas-lista").html(data["html-card-pessoas"]);
    }
    if ("id_pessoa" in data) {
        $(".js-pessoas").attr("data-id_pessoa", data["id_pessoa"]);
    }
    if (data["html-card-pessoa"]) {
        $(".card-pessoa").html(data["html-card-pessoa"]);
    }
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
        data: {
            filtro: pessoasFiltro(),
            busca: $(".js-pessoa-busca").val(),
            id_pessoa: pessoasSelecionada(),
        },
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

// Ao trocar o filtro a seleção é desfeita e o card de detalhes volta vazio
$(document).on("click", ".js-pessoa-filtro", function() {
    $(".js-pessoas").attr("data-id_pessoa", "");
    pessoasMarcaFiltro($(this).data("filtro"));
    pessoasCarrega();
});

var pessoasEspera = null;

$(document).on("input", ".js-pessoa-busca", function() {
    clearTimeout(pessoasEspera);
    pessoasEspera = setTimeout(pessoasCarrega, 350);
});

// Abre a pessoa no card de detalhes (clique na linha ou no botão)
$(document).on("click", ".js-pessoa-selecionar", function() {
    var linha = $(this);
    var id = linha.data("id_pessoa");
    pessoasAjax(linha.data("url"), "GET", {id_pessoa: id}, function(data) {
        if (pessoasSessaoExpirada(data)) {
            return;
        }
        $(".js-pessoa-selecionar").removeClass("ui-linha-ativa");
        linha.addClass("ui-linha-ativa");
        $(".js-pessoas").attr("data-id_pessoa", id);
        pessoasAtualiza(data);
        // Em telas estreitas o card de detalhes fica abaixo da lista
        if (window.matchMedia("(max-width: 1200px)").matches) {
            $("html, body").animate({scrollTop: $(".card-pessoa").offset().top - 10}, 200);
        }
    });
});

// Modal de novo e alterar

function pessoaMascaras(modal) {
    modal.find("[data-mascara]").each(function() {
        $(this).mask($(this).data("mascara"));
    });
}

// Mostra só os documentos do tipo escolhido: CNPJ e IE (jurídica)
// ou CPF e RG (física)
function pessoaTipo(modal) {
    var tipo = modal.find("[name=tipo]").val();
    modal.find(".js-pessoa-tipo").each(function() {
        $(this).prop("hidden", $(this).data("tipo") !== tipo);
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
    pessoaTipo(modal);
    form.on("change", "[name=tipo]", function() {
        pessoaTipo(modal);
    });
    modal.find(".modal-footer .btn-save").off("click").on("click", function() {
        form.trigger("submit");
    });
    form.on("submit", function(event) {
        event.preventDefault();
        var dados = form.serialize() + "&" + $.param({filtro: pessoasFiltro()});
        pessoasAjax(form.attr("action"), "POST", dados, function(data) {
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
    pessoasAjax(botao.data("url"), "GET", requestData, function(data) {
        if (pessoasSessaoExpirada(data)) {
            return;
        }
        // Ícones só neste modal; os outros trocam título e botão com .text()
        var icone = botao.data("id_pessoa") ? "bi-pencil-square" : "bi-person-plus";
        modal.find(".modal-title").empty().append(
            $("<i>").addClass("bi " + icone),
            $("<span>").text(botao.data("title"))
        );
        modal.find(".modal-footer .btn-save").empty().append(
            $("<i>").addClass("bi bi-check-lg"),
            $("<span>").text("SALVAR")
        );
        modal.find(".modal-body").html(data["modal_html"]);
        pessoaSubmit(modal);
        // O Bootstrap foca o próprio modal ao terminar de abrir,
        // então o foco no campo só pode ser dado depois disso
        modal.off("shown.bs.modal.pessoa").one("shown.bs.modal.pessoa", function() {
            pessoaFocaCampo(modal);
        });
        // Layout largo e centralizado só para este modal (clientes.css)
        modal.addClass("modal-pessoa");
        modal.off("hidden.bs.modal.pessoa").one("hidden.bs.modal.pessoa", function() {
            modal.removeClass("modal-pessoa");
        });
        modal.modal("show");
    });
});
