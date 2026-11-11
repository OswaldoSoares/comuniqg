# `usuario_consulta`

Arquivo: `account/views.py`

Card de detalhes de um usuário (JSON).

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
@require_GET
def usuario_consulta(request):
    return facade.create_data_usuario(
        request, facade.obter_id(request.GET.get("id_usuario"))
    )
```

## Exemplo de Uso

```{py3 linenums="1"}
# usuario_consulta(request)
```
