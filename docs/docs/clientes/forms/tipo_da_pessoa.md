# `tipo_da_pessoa`

Arquivo: `clientes/forms.py`

Deduz se a pessoa é jurídica ou física. A tabela `pessoa` não tem coluna de tipo, então ele vem dos documentos preenchidos.

## Fluxo de Execução

1. CNPJ ou IE preenchidos: jurídica (`J`).
2. CPF ou RG preenchidos: física (`F`).
3. Sem nenhum documento: física para fornecedor e jurídica para cliente.

## Parâmetros

- `pessoa` (`Pessoa`).

## Retorno

- `str`: `J` ou `F`.

## Dependências

- [`preenchido`](preenchido.md).
- `DOCUMENTOS`.

## Código da Função

```{py3 linenums="1"}
def tipo_da_pessoa(pessoa):
    """Jurídica ou física pelos documentos; sem nenhum, pela função
    (clientes costumam ser empresas e fornecedores, pessoas)."""
    if any(preenchido(getattr(pessoa, c)) for c in DOCUMENTOS[JURIDICA]):
        return JURIDICA
    if any(preenchido(getattr(pessoa, c)) for c in DOCUMENTOS[FISICA]):
        return FISICA
    return FISICA if pessoa.funcao == "FORNECEDOR" else JURIDICA
```

## Exemplo de Uso

```{py3 linenums="1"}
tipo_da_pessoa(pessoa)  # "J"
```
