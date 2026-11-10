# `_dados_pessoa`

Arquivo: `clientes/facade.py`

Lista os dados cadastrais mostrados no card de detalhes. Campos com a máscara zerada do Delphi viram `""` e o template mostra `-`.

## Fluxo de Execução

1. Junta cidade e UF (`SÃO PAULO/SP`) quando as duas estão preenchidas.
2. Devolve pares (rótulo, valor) na ordem da tela.

## Parâmetros

- `pessoa` (`Pessoa`).

## Retorno

- `list[tuple[str, str]]`: CNPJ, Inscrição estadual, CPF, RG, Endereço, Bairro, Cidade, CEP e Site.

## Dependências

- `preenchido(...)`: `clientes/forms.py`.

## Código da Função

```{py3 linenums="1"}
def _dados_pessoa(pessoa):
    cidade = preenchido(pessoa.cidade)
    if cidade and preenchido(pessoa.estado):
        cidade = f"{cidade}/{pessoa.estado}"
    return [
        ("CNPJ", preenchido(pessoa.cnpj)),
        ("Inscrição estadual", preenchido(pessoa.ie)),
        ("CPF", preenchido(pessoa.cpf)),
        ("RG", preenchido(pessoa.rg)),
        ("Endereço", preenchido(pessoa.endereco)),
        ("Bairro", preenchido(pessoa.bairro)),
        ("Cidade", cidade),
        ("CEP", preenchido(pessoa.cep)),
        ("Site", preenchido(pessoa.site)),
    ]
```

## Exemplo de Uso

```{py3 linenums="1"}
dict(_dados_pessoa(pessoa))["CNPJ"]
```
