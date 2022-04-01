import locale


def mp(mm: float) -> float:
    """Convert from millimeters to points - pt-BR   Converte de milimetros para pontos. 

    Args:
        mm (float): millimeters

    Returns:
        float: points
    """
    return mm / 0.352777


def c_br(valor: str) -> str:
    locale.setlocale(locale.LC_ALL, 'pt_BR')
    valor_br = locale.currency(valor, grouping=True, symbol=True)
    valor_br = valor_br.replace('R$', 'R$ ')
    return valor_br