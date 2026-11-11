# `usuarios.js`

Arquivo: `core/static/core/js/usuarios.js`, carregado só em `account/usuarios.html`. Usa as funções de [`ui.js`](../core/ui-js.md) para ajax e modal.

## Funções

| Função | O que faz |
|---|---|
| `usuariosFiltro()` | Filtro atual, lido de `data-filtro` do card. |
| `usuariosMarcaFiltro(filtro)` | Destaca o botão do filtro e atualiza `aria-pressed`. |
| `usuariosSelecionado()` | Id do usuário aberto no card de detalhes (`data-id_usuario`), ou `""`. |
| `usuariosAtualiza(data)` | Aplica a resposta JSON: lista (`html-card-usuarios`), seleção (`id_usuario`), detalhes (`html-card-usuario`), filtro, busca e toast. |
| `usuariosCarrega()` | Recarrega a lista sem o loader de tela cheia. Usa um contador para ignorar respostas antigas. |

## Eventos

| Seletor | Evento | Ação |
|---|---|---|
| `.js-usuario-filtro` | click | Desfaz a seleção, marca o filtro e recarrega a lista. |
| `.js-usuario-busca` | input | Recarrega a lista 350 ms depois da última tecla. |
| `.js-usuario-selecionar` | click | Abre o usuário no card de detalhes (`usuario_consulta`). Em telas estreitas, rola até o card. |
| `.js-usuario-abrir` | click | Abre o modal indicado em `data-url` (novo, alterar ou nova senha) com `uiModalAbre`, usando `data-title` e `data-icone`. |
| `.js-usuario-situacao` | click | Ativa ou inativa por POST. Ao inativar, pede confirmação (`data-confirmar`). O token CSRF vem do `{% csrf_token %}` da página. |
