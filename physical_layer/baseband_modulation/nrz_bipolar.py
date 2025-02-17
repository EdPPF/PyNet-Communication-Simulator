"""Modulação banda base NRZ Bipolar."""

def bipolar_nrz(data: list[int]) -> list[int]:
    """
    Aplica a modulação NRZ Bipolar aos dados.\n
    '0' é representado como 0 e '1' alterna entre 1 e -1.
    """
    modulated_data = []
    current_polarity = 1 # Começa com 1
    for bit in data:
        if bit == 0:
            modulated_data.append(0)
        else:
            modulated_data.append(current_polarity)
            current_polarity *= -1 # Alterna a polaridade
    return modulated_data

def demodulate_bipolar_nrz(modulated_data: list[int]) -> list[int]:
    """
    Aplica a demodulação NRZ Bipolar aos dados modulados.\n
    0 é representado como '0' e qualquer outro valor como '1'.
    """
    return [0 if bit == 0 else 1 for bit in modulated_data]
