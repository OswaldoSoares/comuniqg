# `get_usuarios`

Arquivo: `account/facade.py`

Usuários da lista, filtrados pela situação e pela busca.

## Fluxo de Execução

1. `ATIVOS` ou `INATIVOS` filtram por `is_active`.
2. A busca procura no nome, no sobrenome e no e-mail.
3. Ordena por nome, sobrenome e e-mail.

## Parâmetros

- `filtro` (`str`).
- `busca` (`str`).

## Retorno

- `QuerySet[Account]`.

## Dependências

- `Account`, `Q`.

## Código da Função

```{py3 linenums="1"}
def get_usuarios(filtro=FILTRO_PADRAO, busca=""):
    usuarios = Account.objects.all()
    if filtro == "ATIVOS":
        usuarios = usuarios.filter(is_active=True)
    elif filtro == "INATIVOS":
        usuarios = usuarios.filter(is_active=False)

    busca = " ".join((busca or "").split())
    if busca:
        usuarios = usuarios.filter(
            Q(first_name__icontains=busca)
            | Q(last_name__icontains=busca)
            | Q(email__icontains=busca)
        )
    return usuarios.order_by("first_name", "last_name", "email")
```

## Exemplo de Uso

```{py3 linenums="1"}
get_usuarios("TODOS", "maria")
```
