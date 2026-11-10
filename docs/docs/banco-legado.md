# Banco legado (Delphi)

O banco MySQL de produção é compartilhado com o aplicativo desktop em Delphi. Enquanto o Delphi estiver em uso, a estrutura das tabelas dele **não pode mudar** (nenhuma coluna, índice ou tabela nova nelas).

## Como as tabelas são usadas no Django

- Models em `databaseold/models.py`, todos com `managed = False`: o `migrate` não mexe nelas.
- Tabelas MyISAM, codificação **latin1**: caracteres fora do latin1 (emoji, aspas curvas) são recusados no formulário.
- Todas as colunas são `NOT NULL` sem valor padrão, e o MySQL está em modo estrito: todo campo precisa ser enviado no `INSERT`.
- Nos testes, o `conftest.py` marca esses models como `managed = True` para o banco de teste criar as tabelas.

## Convenções que o Delphi usa

Para o Delphi continuar lendo os cadastros feitos no Django, gravamos do mesmo jeito que ele.

| Campo | Vazio é gravado como |
|---|---|
| CNPJ | `00.000.000/0000-00` |
| CPF | `000.000.000-00` |
| Inscrição estadual | `000.000.000.000` |
| RG | `00.000.000-0` |
| CEP | `00000-000` |
| Telefones do contato | `(00)00000-0000` |
| Nascimento do contato | `2012-01-01` |
| Endereço, bairro, site | `''` |
| Observação (`OBS`) | `NULL` |

- Textos em **maiúsculas** (o site em minúsculas).
- `Ativo`: todos os cadastros estão com `'S'`. Ainda não sabemos se o Delphi respeita `'N'`, por isso o Django grava `'S'` no cadastro novo e não muda o valor na alteração.
- Ao mostrar um campo, a máscara zerada aparece vazia (ou `-`): veja [`preenchido`](clientes/forms/preenchido.md).

## Ligações entre tabelas

Não há chaves estrangeiras declaradas; as ligações são por id numérico.

| Tabela | Coluna | Aponta para |
|---|---|---|
| `contato` | `IDPessoa` | `pessoa` |
| `servico` | `IDCadastro` | `pessoa` (cliente) |
| `pagar` | `IDPessoa` | `pessoa` (fornecedor) |
