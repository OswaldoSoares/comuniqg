# `_movimento`

Arquivo: `clientes/facade.py`

Indicadores do card de detalhes: quantidade e data do último serviço (cliente) ou da última conta a pagar (fornecedor).

## Fluxo de Execução

1. Fornecedor: conta as linhas de `pagar` por `IDPessoa` e pega o maior `DiaServico`.
2. Cliente: conta as linhas de `servico` por `IDCadastro` e pega o maior `DiaServico`.

## Parâmetros

- `pessoa` (`Pessoa`).

## Retorno

- `dict`: `rotulo`, `ultimo_rotulo`, `quantidade` e `ultimo` (`date` ou `None`).

## Dependências

- `Pagar`, `Servico` (`databaseold`).
- `Count`, `Max`.

## Código da Função

```{py3 linenums="1"}
def _movimento(pessoa):
    """Serviços do cliente ou contas a pagar do fornecedor."""
    if pessoa.funcao == "FORNECEDOR":
        totais = Pagar.objects.filter(idpessoa=pessoa.pk).aggregate(
            quantidade=Count("idpagar"), ultimo=Max("diaservico")
        )
        return {
            "rotulo": "Contas a pagar",
            "ultimo_rotulo": "Última conta",
            **totais,
        }
    totais = Servico.objects.filter(idcadastro=pessoa.pk).aggregate(
        quantidade=Count("idservico"), ultimo=Max("diaservico")
    )
    return {"rotulo": "Serviços", "ultimo_rotulo": "Último serviço", **totais}
```

## Exemplo de Uso

```{py3 linenums="1"}
movimento = _movimento(pessoa)
movimento["quantidade"]
```
