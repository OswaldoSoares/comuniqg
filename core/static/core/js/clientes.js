// Cadastro de clientes e fornecedores (clientes/index.html).
// Ajax e modal vêm de ui.js.

function pessoasFiltro() {
    return $(".js-pessoas").attr("data-filtro") || "";
}

function pessoasMarcaFiltro(filtro) {
    $(".js-pessoas").attr("data-filtro", filtro);
    $(".js-pessoa-filtro").each(function() {
        var ativo = $(this).data("filtro") === filtro;
        $(this).toggleClass("ui-filtro-ativo", ativo);
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
            if (numero !== pessoasRequisicao || uiSessaoExpirada(data)) {
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
    uiAjax(linha.data("url"), "GET", {id_pessoa: id}, function(data) {
        if (uiSessaoExpirada(data)) {
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
    modal.find(".js-campo-grupo").each(function() {
        $(this).prop("hidden", $(this).data("grupo") !== tipo);
    });
}

// Máscaras e documentos do tipo; refeito quando o form volta com erro
function pessoaPreparaForm(modal) {
    pessoaMascaras(modal);
    pessoaTipo(modal);
    modal.find("[name=tipo]").on("change", function() {
        pessoaTipo(modal);
    });
}

$(document).on("click", ".js-pessoa-abrir", function() {
    var botao = $(this);
    var requestData = {};
    if (botao.data("id_pessoa")) {
        requestData["id_pessoa"] = botao.data("id_pessoa");
    }
    uiAjax(botao.data("url"), "GET", requestData, function(data) {
        if (uiSessaoExpirada(data)) {
            return;
        }
        uiModalAbre({
            titulo: botao.data("title"),
            icone: botao.data("id_pessoa") ? "bi-pencil-square" : "bi-person-plus",
            html: data["modal_html"],
            aoCarregar: pessoaPreparaForm,
            dadosExtras: function() {
                return {filtro: pessoasFiltro()};
            },
            aoSalvar: pessoasAtualiza,
        });
    });
});
