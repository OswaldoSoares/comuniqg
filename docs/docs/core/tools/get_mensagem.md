# `get_mensagem`

Arquivo: `core/tools.py`

Monta a mensagem do toast a partir de um código de `core/message.py`.

## Fluxo de Execução

1. Busca o código em `mensagens`; se não existir, devolve "Mensagem não encontrada." (tipo `info`).
2. Formata o texto com os parâmetros (`{apelido}` etc.).
3. Se faltar parâmetro, devolve o aviso em vez de gerar erro.

## Parâmetros

- `codigo` (`str`): Ex.: `clca0001`.
- `**kwargs`: Valores para o texto.

## Retorno

- `dict`: `mensagem` e `tipo` (`success`, `info`, `warning` ou `error`), as chaves que o JS usa no toastr.

## Dependências

- `core.message.mensagens`.

## Código da Função

```{py3 linenums="1"}
def get_mensagem(codigo, **kwargs):
    """Mensagem pronta para o toast: {"mensagem": ..., "tipo": ...}."""
    msg_data = mensagens.get(codigo)
    if not msg_data:
        return {"mensagem": "Mensagem não encontrada.", "tipo": "info"}

    try:
        mensagem_formatada = msg_data["mensagem"].format(**kwargs)
    except KeyError as e:
        mensagem_formatada = (
            f"erro ao formatar mensagem: parâmetro ausente ({e})"
        )

    return {"mensagem": mensagem_formatada, "tipo": msg_data["tipo"]}
```

## Exemplo de Uso

```{py3 linenums="1"}
get_mensagem("clca0001", funcao="CLIENTE", apelido="ACME")
# {"mensagem": "CLIENTE ACME ADICIONADO COM SUCESSO.", "tipo": "success"}
```
