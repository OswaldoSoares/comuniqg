# Mensagens do sistema, obtidas com core.tools.get_mensagem.
#
# Código: 2 letras do app + 2 letras do assunto + 4 dígitos.
# Ex.: "clca0001" = clientes / cadastro, mensagem 1.
# "mensagem" aceita parâmetros no formato {nome}, passados ao get_mensagem.
# "tipo" é o estilo do toast: success, info, warning ou error.
mensagens = {
    "clca0001": {
        "mensagem": "{funcao} {apelido} ADICIONADO COM SUCESSO.",
        "tipo": "success",
    },
    "clca0002": {
        "mensagem": "{funcao} {apelido} ALTERADO COM SUCESSO.",
        "tipo": "success",
    },
}
