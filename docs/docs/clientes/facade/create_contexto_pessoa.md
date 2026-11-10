# `create_contexto_pessoa`

Arquivo: `clientes/facade.py`

Monta o contexto do card de detalhes da pessoa selecionada.

## Fluxo de Execução

1. Busca a pessoa; retorna 404 se não existir.
2. Junta os dados cadastrais, os contatos e o movimento.

## Parâmetros

- `id_pessoa` (`int`).

## Retorno

- `dict`: `pessoa`, `dados`, `contatos`, `movimento`.

## Dependências

- `get_object_or_404(...)`.
- [`_dados_pessoa`](_dados_pessoa.md), [`_contatos`](_contatos.md), [`_movimento`](_movimento.md).

## Código da Função

```{py3 linenums="1"}
def create_contexto_pessoa(id_pessoa):
    """Dados da pessoa selecionada para o card de detalhes."""
    pessoa = get_object_or_404(Pessoa, pk=id_pessoa)
    return {
        "pessoa": pessoa,
        "dados": _dados_pessoa(pessoa),
        "contatos": _contatos(pessoa.pk),
        "movimento": _movimento(pessoa),
    }
```

## Exemplo de Uso

```{py3 linenums="1"}
contexto = create_contexto_pessoa(15)
contexto["pessoa"].apelido
```
