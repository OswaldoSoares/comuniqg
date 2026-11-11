# Clientes e fornecedores

Cadastro da tabela `pessoa` (do Delphi), no padrão de tela de veículos do projeto efetiva. Endereço: `/clientes/` (menu **CADASTRO**).

## Tela

- **Lista** (esquerda): apelido, nome e função. Filtros Clientes (padrão), Fornecedores e Todos, e busca por apelido, nome, CNPJ ou CPF (com ou sem pontuação, a partir de 3 dígitos). A busca espera 350 ms depois da última tecla.
- **Detalhes** (direita): ao clicar numa linha (ou na seta), mostra:
  - os dados cadastrais e a observação;
  - os contatos (tabela `contato`, só leitura);
  - a quantidade de serviços e a data do último (cliente), ou de contas a pagar e da última (fornecedor);
  - o botão alterar.
- Ao trocar o filtro, a seleção é desfeita e o card de detalhes volta para "Selecione um cadastro na lista para ver os detalhes". A busca mantém a pessoa aberta.
- Em telas com menos de 1200px, o card de detalhes fica abaixo da lista.
- `/clientes/?id_pessoa=<id>` abre a tela com a pessoa selecionada.

## Modal (novo e alterar)

- Centralizado, com 960px e visual `ui-*` (classe `modal-ui`, posta por `uiModalAbre` em [`ui.js`](../core/ui-js.md)). Os modais das telas antigas não mudam.
- Primeira linha: **Pessoa** (jurídica ou física), **Função** (cliente ou fornecedor) e **Apelido**.
- Jurídica mostra CNPJ e Inscrição estadual; física mostra CPF e RG.
- Ao salvar, a lista vai para o filtro da função salva, a busca é limpa e a pessoa salva abre no card de detalhes.

## Regras do cadastro

- A tabela não tem coluna de tipo: ele é deduzido dos documentos ([`tipo_da_pessoa`](forms/tipo_da_pessoa.md)). Os documentos do outro tipo são gravados como máscara zerada.
- **Apelido**: obrigatório e sem repetir (sem diferenciar maiúsculas).
- **Nome** e **Função**: obrigatórios.
- **CNPJ e CPF**: dígitos verificadores conferidos, gravados com máscara e sem repetir.
- **IE**: com 12 dígitos é formatada; texto como `ISENTO` fica como digitado.
- **CEP**: 8 dígitos.
- Campos vazios seguem as [convenções do Delphi](../banco-legado.md).
- Cadastro novo grava `Ativo = 'S'`. Inativar e excluir ainda não existem: excluir é arriscado enquanto o Delphi usa o mesmo banco.

## Endereços

| URL | View | Uso |
|---|---|---|
| `/clientes/?filtro=&busca=&id_pessoa=` | [`index_clientes`](views/index_clientes.md) | página |
| `/clientes/pessoas` | [`pessoas_lista`](views/pessoas_lista.md) | lista e detalhes (JSON) |
| `/clientes/pessoa` | [`pessoa_consulta`](views/pessoa_consulta.md) | card de detalhes (JSON) |
| `/clientes/pessoa/form` | [`pessoa_form`](views/pessoa_form.md) | GET abre o modal, POST salva |

Todas exigem login. Mensagens em `core/message.py`: `clca0001` (adicionado) e `clca0002` (alterado).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `clientes/facade.py` | busca, contextos, respostas JSON e gravação |
| `clientes/forms.py` | `CadastraPessoa` e as funções de documento |
| `clientes/html_data.py` | renderização dos pedaços de HTML |
| `clientes/templates/clientes/index.html` | página |
| `clientes/templates/clientes/components/pessoas.html` | lista |
| `clientes/templates/clientes/components/pessoa.html` | card de detalhes |
| `clientes/templates/clientes/modal_pessoa.html` | formulário do modal (campos com `core/components/campo.html`) |
| `core/static/core/js/clientes.js` | [comportamento da tela](javascript.md) |
| `core/static/core/css/clientes.css` | selos cliente/fornecedor e contatos (a base vem de [`ui-cadastro.css`](../padrao-visual.md#telas-de-cadastro)) |
| `clientes/tests/` | testes do form e das views |
