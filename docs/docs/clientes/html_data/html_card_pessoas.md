# `html_card_pessoas`

Arquivo: `clientes/html_data.py`

Renderiza a lista (`clientes/components/pessoas.html`) na chave `html-card-pessoas`.

## Fluxo de Execução

1. Renderiza o template com o contexto.
2. Grava no dicionário `data`.

## Parâmetros

- `request`, `contexto` (`dict`), `data` (`dict`).

## Retorno

- `dict`: o próprio `data`.

## Dependências

- `render_to_string`.

## Código da Função

```{py3 linenums="1"}
def html_card_pessoas(request, contexto, data):
    data["html-card-pessoas"] = render_to_string(
        "clientes/components/pessoas.html", contexto, request=request
    )
    return data
```

## Exemplo de Uso

```{py3 linenums="1"}
data = html_card_pessoas(request, contexto, {})
```
