# `get_pessoas`

Arquivo: `clientes/facade.py`

Busca as pessoas da lista, filtradas pela função e pelo texto digitado na busca.

## Fluxo de Execução

1. Parte de todas as pessoas; se o filtro não for `TODOS`, filtra pela função.
2. Junta espaços repetidos da busca.
3. Com busca, procura no apelido e no nome (sem diferenciar maiúsculas).
4. Se a busca tiver 3 dígitos ou mais, procura também nos dígitos do CNPJ e do CPF (`_sem_pontuacao`).
5. Ordena por apelido e id.

## Parâmetros

- `filtro` (`str`): `CLIENTE`, `FORNECEDOR` ou `TODOS`.
- `busca` (`str`): Texto digitado; vazio traz todos.

## Retorno

- `QuerySet[Pessoa]`: Pessoas encontradas.

## Dependências

- `so_digitos(...)`: Dígitos da busca (`clientes/forms.py`).
- [`_sem_pontuacao`](_sem_pontuacao.md): Documento sem máscara no SQL.

## Código da Função

```{py3 linenums="1"}
def get_pessoas(filtro=FILTRO_PADRAO, busca=""):
    pessoas = Pessoa.objects.all()
    if filtro != "TODOS":
        pessoas = pessoas.filter(funcao=filtro)

    busca = " ".join((busca or "").split())
    if busca:
        condicao = Q(apelido__icontains=busca) | Q(nome__icontains=busca)
        digitos = so_digitos(busca)
        if len(digitos) >= 3:
            pessoas = pessoas.annotate(
                cnpj_digitos=_sem_pontuacao("cnpj"),
                cpf_digitos=_sem_pontuacao("cpf"),
            )
            condicao |= Q(cnpj_digitos__contains=digitos) | Q(
                cpf_digitos__contains=digitos
            )
        pessoas = pessoas.filter(condicao)

    return pessoas.order_by("apelido", "idpessoa")
```

## Exemplo de Uso

```{py3 linenums="1"}
get_pessoas("TODOS", "11222333")  # CNPJ 11.222.333/...
get_pessoas("CLIENTE", "acme")
```
