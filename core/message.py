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
    "acus0001": {
        "mensagem": "USUÁRIO {email} ADICIONADO COM SUCESSO.",
        "tipo": "success",
    },
    "acus0002": {
        "mensagem": "USUÁRIO {email} ALTERADO COM SUCESSO.",
        "tipo": "success",
    },
    "acus0003": {
        "mensagem": "SENHA DE {email} ALTERADA COM SUCESSO.",
        "tipo": "success",
    },
    "acus0004": {
        "mensagem": "USUÁRIO {email} ATIVADO.",
        "tipo": "success",
    },
    "acus0005": {
        "mensagem": "USUÁRIO {email} INATIVADO. ELE NÃO CONSEGUE MAIS ENTRAR.",
        "tipo": "warning",
    },
    "acus0006": {
        "mensagem": "VOCÊ NÃO PODE INATIVAR O SEU PRÓPRIO USUÁRIO.",
        "tipo": "error",
    },
}
