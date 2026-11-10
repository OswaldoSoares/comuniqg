# `clientes.js`

Arquivo: `core/static/core/js/clientes.js`, carregado só em `clientes/index.html`. Usa jQuery, jQuery Mask, o modal do Bootstrap 3 e `mostrarToast` (`base.js`).

## Funções

| Função | O que faz |
|---|---|
| `pessoasAjax(url, type, data, sucessoCallback)` | Igual ao `executarAjax` (`ajax.js`): mostra o loader e, em erro, mostra um toast. A diferença é que **não volta ao topo da página**, para não perder a posição na lista. |
| `pessoasSessaoExpirada(data)` | Se a resposta não for JSON (o Django devolveu a tela de login), recarrega a página e retorna `true`. |
| `pessoasFiltro()` | Filtro atual, lido de `data-filtro` do card. |
| `pessoasMarcaFiltro(filtro)` | Destaca o botão do filtro e atualiza `aria-pressed`. |
| `pessoasSelecionada()` | Id da pessoa aberta no card de detalhes (`data-id_pessoa`), ou `""`. |
| `pessoasAtualiza(data)` | Aplica a resposta JSON: lista (`html-card-pessoas`), seleção (`id_pessoa`), detalhes (`html-card-pessoa`), filtro, busca e toast (`mensagem`/`tipo`). |
| `pessoasCarrega()` | Recarrega a lista sem o loader de tela cheia. Usa um contador para ignorar respostas antigas quando a busca muda rápido. |
| `pessoaMascaras(modal)` | Aplica as máscaras dos campos com `data-mascara`. |
| `pessoaTipo(modal)` | Mostra só os documentos do tipo escolhido (campos com `data-tipo`). |
| `pessoaFocaCampo(modal)` | Foca o primeiro campo com erro ou, se não houver erro, o primeiro campo. |
| `pessoaSubmit(modal)` | Liga máscaras, tipo e botão salvar, e envia o form por ajax com o filtro atual. Com erro, troca o form pelo `html_form`; sem erro, fecha o modal e atualiza a tela. |

## Eventos

| Seletor | Evento | Ação |
|---|---|---|
| `.js-pessoa-filtro` | click | Desfaz a seleção, marca o filtro e recarrega a lista. |
| `.js-pessoa-busca` | input | Recarrega a lista 350 ms depois da última tecla. |
| `.js-pessoa-selecionar` | click | Abre a pessoa no card de detalhes (`pessoa_consulta`). Em telas estreitas, rola até o card. |
| `.js-pessoa-abrir` | click | Abre o modal de cadastro (sem `data-id_pessoa`) ou de alteração. Põe ícones no título e no botão salvar, e a classe `modal-pessoa` enquanto o modal está aberto. |
