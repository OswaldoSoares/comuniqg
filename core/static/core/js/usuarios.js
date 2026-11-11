// Tela de usuários (account/usuarios.html). Ajax e modal vêm de ui.js.

function usuariosFiltro() {
    return $(".js-usuarios").attr("data-filtro") || "";
}

function usuariosMarcaFiltro(filtro) {
    $(".js-usuarios").attr("data-filtro", filtro);
    $(".js-usuario-filtro").each(function() {
        var ativo = $(this).data("filtro") === filtro;
        $(this).toggleClass("ui-filtro-ativo", ativo);
        $(this).attr("aria-pressed", ativo ? "true" : "false");
    });
}

// Usuário aberto no card de detalhes
function usuariosSelecionado() {
    return $(".js-usuarios").attr("data-id_usuario") || "";
}

function usuariosAtualiza(data) {
    if (data["html-card-usuarios"]) {
        $(".card-usuarios-lista").html(data["html-card-usuarios"]);
    }
    if ("id_usuario" in data) {
        $(".js-usuarios").attr("data-id_usuario", data["id_usuario"]);
    }
    if (data["html-card-usuario"]) {
        $(".card-usuario").html(data["html-card-usuario"]);
    }
    if (data["filtro"]) {
        usuariosMarcaFiltro(data["filtro"]);
    }
    if (typeof data["busca"] === "string" && $(".js-usuario-busca").val() !== data["busca"]) {
        $(".js-usuario-busca").val(data["busca"]);
    }
    if (data["mensagem"]) {
        mostrarToast(data["mensagem"], data["tipo"]);
    }
}

// Lista: filtro e busca sem o loader de tela cheia, para não piscar
// a cada tecla; só a resposta da última busca é usada.
var usuariosRequisicao = 0;

function usuariosCarrega() {
    var numero = ++usuariosRequisicao;
    $.ajax({
        type: "GET",
        url: $(".js-usuarios").data("url-lista"),
        data: {
            filtro: usuariosFiltro(),
            busca: $(".js-usuario-busca").val(),
            id_usuario: usuariosSelecionado(),
        },
        success: function(data) {
            if (numero !== usuariosRequisicao || uiSessaoExpirada(data)) {
                return;
            }
            usuariosAtualiza(data);
        },
        error: function(error) {
            console.log("ERROR: ", error);
        }
    });
}

// Ao trocar o filtro a seleção é desfeita e o card de detalhes volta vazio
$(document).on("click", ".js-usuario-filtro", function() {
    $(".js-usuarios").attr("data-id_usuario", "");
    usuariosMarcaFiltro($(this).data("filtro"));
    usuariosCarrega();
});

var usuariosEspera = null;

$(document).on("input", ".js-usuario-busca", function() {
    clearTimeout(usuariosEspera);
    usuariosEspera = setTimeout(usuariosCarrega, 350);
});

// Abre o usuário no card de detalhes (clique na linha ou na seta)
$(document).on("click", ".js-usuario-selecionar", function() {
    var linha = $(this);
    var id = linha.data("id_usuario");
    uiAjax(linha.data("url"), "GET", {id_usuario: id}, function(data) {
        if (uiSessaoExpirada(data)) {
            return;
        }
        $(".js-usuario-selecionar").removeClass("ui-linha-ativa");
        linha.addClass("ui-linha-ativa");
        $(".js-usuarios").attr("data-id_usuario", id);
        usuariosAtualiza(data);
        // Em telas estreitas o card de detalhes fica abaixo da lista
        if (window.matchMedia("(max-width: 1200px)").matches) {
            $("html, body").animate({scrollTop: $(".card-usuario").offset().top - 10}, 200);
        }
    });
});

// Modais de novo, alterar e nova senha (data-url diz qual)
$(document).on("click", ".js-usuario-abrir", function() {
    var botao = $(this);
    var requestData = {};
    if (botao.data("id_usuario")) {
        requestData["id_usuario"] = botao.data("id_usuario");
    }
    uiAjax(botao.data("url"), "GET", requestData, function(data) {
        if (uiSessaoExpirada(data)) {
            return;
        }
        uiModalAbre({
            titulo: botao.data("title"),
            icone: botao.data("icone"),
            html: data["modal_html"],
            dadosExtras: function() {
                return {filtro: usuariosFiltro()};
            },
            aoSalvar: usuariosAtualiza,
        });
    });
});

// Ativar / inativar, com confirmação ao inativar
$(document).on("click", ".js-usuario-situacao", function() {
    var botao = $(this);
    if (botao.data("confirmar") && !window.confirm(botao.data("confirmar"))) {
        return;
    }
    var dados = {
        id_usuario: botao.data("id_usuario"),
        filtro: usuariosFiltro(),
        csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").first().val(),
    };
    uiAjax(botao.data("url"), "POST", dados, function(data) {
        if (uiSessaoExpirada(data)) {
            return;
        }
        usuariosAtualiza(data);
    });
});
