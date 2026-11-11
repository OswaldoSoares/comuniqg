# `usuario_situacao`

Arquivo: `account/views.py`

POST ativa ou inativa.

## Fluxo de Execução

1. Exige administrador ([`administrador_required`](../decorators/administrador_required.md)).
2. Chama a função do facade correspondente.

## Parâmetros

- `request` (`HttpRequest`).

## Retorno

- `HttpResponse` ou `JsonResponse`.

## Dependências

- `account/facade.py`.

## Código da Função

```{py3 linenums="1"}
@administrador_required
@require_POST
def usuario_situacao(request):
    return facade.alterar_situacao_usuario(request)
```

## Exemplo de Uso

```{py3 linenums="1"}
# usuario_situacao(request)
```
