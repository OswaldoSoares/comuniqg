# `html_card_pessoa`

Arquivo: `clientes/html_data.py`

Renderiza o card de detalhes (`clientes/components/pessoa.html`) na chave `html-card-pessoa`. Com contexto vazio, mostra "Selecione um cadastro na lista...".

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
def html_card_pessoa(request, contexto, data):
    data["html-card-pessoa"] = render_to_string(
        "clientes/components/pessoa.html", contexto, request=request
    )
    return data
```

## Exemplo de Uso

```{py3 linenums="1"}
data = html_card_pessoa(request, {}, data)  # card vazio
```
