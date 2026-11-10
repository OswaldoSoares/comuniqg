# `_contatos`

Arquivo: `clientes/facade.py`

Lê os contatos da pessoa (tabela `contato`, só leitura) para o card de detalhes.

## Fluxo de Execução

1. Busca os contatos por `idpessoa`, ordenados por nome.
2. Para cada contato, junta os telefones e celulares preenchidos (`(00)00000-0000` é ignorado) e o e-mail.

## Parâmetros

- `id_pessoa` (`int`).

## Retorno

- `list[dict]`: Cada item com `nome`, `fones` (lista) e `email`.

## Dependências

- `Contato` (`databaseold`).
- `preenchido(...)`.

## Código da Função

```{py3 linenums="1"}
def _contatos(id_pessoa):
    contatos = []
    for contato in Contato.objects.filter(idpessoa=id_pessoa).order_by(
        "contato", "idcontato"
    ):
        fones = [
            preenchido(fone)
            for fone in (
                contato.telefone1,
                contato.telefone2,
                contato.celular1,
                contato.celular2,
            )
        ]
        contatos.append(
            {
                "nome": preenchido(contato.contato),
                "fones": [fone for fone in fones if fone],
                "email": preenchido(contato.email),
            }
        )
    return contatos
```

## Exemplo de Uso

```{py3 linenums="1"}
_contatos(15)
# [{"nome": "JOAO", "fones": ["(11)91234-5678"], "email": ""}]
```
