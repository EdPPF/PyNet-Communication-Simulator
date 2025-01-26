"""Modulação banda base Manchester."""

def manchester(data: list[int]) -> list[int]:
    """
    Aplica a modulação Manchester aos dados.\n
    '0' é representado como [1, -1] e '1' como [-1, 1].
    """
    modulated_data = []
    for bit in data:
        if bit == 0:
            modulated_data.extend([1, -1])
        else:
            modulated_data.extend([-1, 1])
    return modulated_data

def demodulate_manchester(modulated_data: list[int]) -> list[int]:
    """
    Aplica a demodulação Manchester aos dados modulados.\n
    Analisa pares de bits para recuperar os valores originais.
    """
    if len(modulated_data) % 2 != 0:
        raise ValueError("Número ímpar de bits na modulação Manchester.")

    demodulated_data = []
    for i in range(0, len(modulated_data), 2):
        transition = modulated_data[i:i+2]
        if transition == [1, -1]:
            demodulated_data.append(0)
        elif transition == [-1, 1]:
            demodulated_data.append(1)
        else:
            raise ValueError(f"Codificação Manchester inválida detectada.")
    return demodulated_data
