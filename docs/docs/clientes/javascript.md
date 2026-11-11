# `clientes.js`

Arquivo: `core/static/core/js/clientes.js`, carregado só em `clientes/index.html`. Usa jQuery, jQuery Mask, `mostrarToast` (`base.js`) e as funções de [`ui.js`](../core/ui-js.md) para ajax e modal.

## Funções

| Função | O que faz |
|---|---|
| `pessoasFiltro()` | Filtro atual, lido de `data-filtro` do card. |
| `pessoasMarcaFiltro(filtro)` | Destaca o botão do filtro e atualiza `aria-pressed`. |
| `pessoasSelecionada()` | Id da pessoa aberta no card de detalhes (`data-id_pessoa`), ou `""`. |
| `pessoasAtualiza(data)` | Aplica a resposta JSON: lista (`html-card-pessoas`), seleção (`id_pessoa`), detalhes (`html-card-pessoa`), filtro, busca e toast (`mensagem`/`tipo`). |
| `pessoasCarrega()` | Recarrega a lista sem o loader de tela cheia. Usa um contador para ignorar respostas antigas quando a busca muda rápido. |
| `pessoaMascaras(modal)` | Aplica as máscaras dos campos com `data-mascara`. |
| `pessoaTipo(modal)` | Mostra só os documentos do tipo escolhido (campos com `data-grupo`). |
| `pessoaPreparaForm(modal)` | Aplica as máscaras e o tipo e liga a troca de tipo. É chamada por `uiModalForm` ao abrir o modal e cada vez que o formulário volta com erro. |

## Eventos

| Seletor | Evento | Ação |
|---|---|---|
| `.js-pessoa-filtro` | click | Desfaz a seleção, marca o filtro e recarrega a lista. |
| `.js-pessoa-busca` | input | Recarrega a lista 350 ms depois da última tecla. |
| `.js-pessoa-selecionar` | click | Abre a pessoa no card de detalhes (`pessoa_consulta`). Em telas estreitas, rola até o card. |
| `.js-pessoa-abrir` | click | Busca o formulário e abre com `uiModalAbre`: cadastro (sem `data-id_pessoa`) ou alteração. Ao salvar, envia o filtro atual e aplica a resposta com `pessoasAtualiza`. |
