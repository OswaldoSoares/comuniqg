# Padrão visual (ui-*)

Padrão copiado do projeto efetiva para modernizar o sistema aos poucos. A referência completa fica na documentação do efetiva.

- Arquivo: `core/static/core/css/ui.css`, carregado no `core/templates/core/base_restrito.html`.
- Todas as classes começam com `ui-`: as telas antigas não são afetadas.
- Estilos específicos de um módulo ficam em um CSS próprio (ex.: `core/static/core/css/clientes.css`), usando as classes `ui-*` como base.

## Cores (variáveis)

| Variável | Valor | Uso |
|---|---|---|
| `--ui-superficie` | `#363636` | fundo do card |
| `--ui-superficie-2` | `#414141` | indicadores e áreas internas |
| `--ui-linha` | branco 8% | separadores da tabela |
| `--ui-texto` | `#f5f5f5` | texto principal |
| `--ui-texto-2` | `#afafaf` | rótulos, subtítulos |
| `--ui-destaque` | `#ffd433` | botão principal, barras, linha ativa |
| `--ui-perigo` | `#ff6b6b` | ações de exclusão |

## Componentes

| Classe | Para que serve |
|---|---|
| `ui-layout-menu`, `ui-menu-lateral`, `ui-menu-item` (+ `ui-menu-ativo`), `ui-layout-conteudo` | menu lateral do módulo: barra estreita com ícone e rótulo curto que acompanha a rolagem (vira abas no celular); a view informa `secao` para marcar o item ativo e o container recebe `ui-conteudo-menu` |
| `ui-card`, `ui-card-header`, `ui-card-titulo`, `ui-card-subtitulo` | card com cabeçalho |
| `ui-secao-titulo` | título de uma seção dentro do card |
| `ui-grid-2`, `ui-grid-3` | duas / três colunas (vira uma no celular) |
| `ui-aviso` | ícone de aviso ao lado de um valor, explicação no `title` |
| `ui-btn ui-btn-primario` | botão de ação principal (amarelo) |
| `ui-btn ui-btn-secundario` | botão secundário (ex.: PDF), funciona em `<a>` |
| `ui-card-acoes` | agrupa os botões do cabeçalho |
| `ui-btn-icone` (+ `ui-perigo`) | botão só com ícone (editar, excluir) |
| `ui-nav-periodo`, `ui-nav-periodo-rotulo` | navegação `< mês >` |
| `ui-kpis`, `ui-kpi`, `ui-kpi-rotulo`, `ui-kpi-valor` | indicadores (4 por linha, 2 no celular) |
| `ui-tabela-wrap`, `ui-tabela` | tabela limpa com rolagem lateral no celular |
| `ui-tabela-cards` | no celular (≤ 600px) cada linha vira um card; cada `<td>` precisa de `data-label="Rótulo"` |
| `ui-col-cheia` | célula que ocupa a linha inteira no modo card (ex.: barra) |
| `ui-num`, `ui-forte`, `ui-acoes` | número alinhado à direita, destaque, coluna de ações |
| `ui-linha-ativa`, `ui-clicavel` | linha selecionada / linha clicável |
| `ui-barra`, `ui-barra-valor` | barra horizontal proporcional dentro da tabela |
| `ui-badge` (cor via `--ui-badge-cor`) | selo com marcador colorido |
| `ui-vazio` | estado de lista vazia |
| `ui-grafico` | container de gráfico Chart.js (altura 240px) |
| `ui-form` | formulário dentro do modal |
| `ui-submit-oculto` | botão submit invisível para salvar com Enter no modal |

## Modal

- Focar o primeiro campo no evento `shown.bs.modal` (antes disso o Bootstrap rouba o foco).
- Datas com `type="date"` (formato `%Y-%m-%d` no widget): o cliente prefere escolher no calendário, mesmo com o Tab passando por dia/mês/ano.
- Em erro de validação, focar o primeiro campo com erro.
- O `style.css` antigo fixa `.modal-dialog` em 500px com `margin-top: 20%` para todos os modais. Para um modal no visual `ui-*`, o JS da tela põe uma classe própria no `#MyModal` ao abrir e tira ao fechar (ex.: `modal-pessoa` em `clientes.js`). Assim os modais antigos não mudam.
- Ícones no título e no botão salvar podem ser postos com `.empty().append(...)`: as outras telas trocam o texto com `.text()`, o que apaga o ícone.

## Regras

- Número em formato brasileiro: `{% load humanize %}` e `{{ valor|intcomma }}` em campos `Decimal`.
- Cor nunca sozinha: badges e barras sempre com o texto/valor ao lado.
- Cores de categorias (ex.: combustíveis) devem ser validadas para daltonismo antes de usar.
- Card em largura total: no CSS do módulo, `.card-xxx.article-card { width: 100%; max-width: 1100px; }`.

## Exemplo

```html
{% load humanize %}
<section class="ui-card">
    <header class="ui-card-header">
        <div>
            <h2 class="ui-card-titulo">Título</h2>
            <p class="ui-card-subtitulo">Subtítulo</p>
        </div>
        <button type="button" class="ui-btn ui-btn-primario">
            <i class="bi bi-plus-lg"></i> Novo
        </button>
    </header>
    <div class="ui-kpis">
        <div class="ui-kpi">
            <span class="ui-kpi-rotulo">Total</span>
            <span class="ui-kpi-valor"><small>R$</small> {{ total|intcomma }}</span>
        </div>
    </div>
    <div class="ui-tabela-wrap">
        <table class="ui-tabela">...</table>
    </div>
</section>
```

Referência neste projeto: `clientes/templates/clientes/index.html` e `clientes/templates/clientes/components/pessoa.html`.
