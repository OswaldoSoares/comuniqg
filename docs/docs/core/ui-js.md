# `ui.js`

Arquivo: `core/static/core/js/ui.js`, carregado em `core/templates/core/base_restrito.html` depois do `ajax.js`. Funções comuns às telas de cadastro no padrão ui (clientes, usuários). Usa jQuery, o modal `#MyModal` do Bootstrap 3 e `mostrarToast` (`base.js`).

## Funções

| Função | O que faz |
|---|---|
| `uiAjax(url, type, data, sucessoCallback)` | Igual ao `executarAjax` (`ajax.js`): mostra o loader e, em erro, mostra um toast. A diferença é que **não volta ao topo da página**, para não perder a posição na lista. |
| `uiSessaoExpirada(data)` | Se a resposta não for JSON (o Django devolveu a tela de login), recarrega a página e retorna `true`. Toda resposta de ajax deve passar por ela. |
| `uiFocaCampo(modal)` | Foca o primeiro campo com erro (dentro de `.ui-campo`) ou, sem erro, o primeiro campo visível. |
| `uiModalForm(modal, opcoes)` | Liga o formulário do modal: chama `opcoes.aoCarregar(modal)`, liga o botão salvar e envia por POST com `opcoes.dadosExtras()`. Se a resposta tiver `html_form`, troca o formulário (com os erros) e liga de novo; senão, fecha o modal e chama `opcoes.aoSalvar(data)`. |
| `uiModalAbre(opcoes)` | Abre o `#MyModal` no visual ui: título com `opcoes.icone`, botão SALVAR com ✓, `opcoes.html` no corpo, foco no campo depois de abrir e a classe `modal-ui` enquanto o modal está aberto. Repassa as opções para `uiModalForm`. |

## Exemplo

```javascript
uiAjax(botao.data("url"), "GET", {id_usuario: id}, function(data) {
    if (uiSessaoExpirada(data)) {
        return;
    }
    uiModalAbre({
        titulo: "ALTERAR USUÁRIO",
        icone: "bi-pencil-square",
        html: data["modal_html"],
        aoCarregar: function(modal) { /* máscaras etc. (opcional) */ },
        dadosExtras: function() { return {filtro: "ATIVOS"}; },
        aoSalvar: usuariosAtualiza,
    });
});
```

O servidor responde ao POST com `{"html_form": ...}` quando há erro, ou com o JSON que `aoSalvar` aplica na tela (lista, card, `mensagem` e `tipo` para o toast).
