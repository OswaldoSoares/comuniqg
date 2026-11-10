from core.message import mensagens


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
