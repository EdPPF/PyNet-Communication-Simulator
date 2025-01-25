def polar_nrz(data: list[int]) -> list[int]:
    """
    Aplica a modulação NRZ Polar aos dados.\n
    Representa '0' como -1 e '1' como 1.
    """
    return [-1 if bit == 0 else 1 for bit in data]

def demodulate_polar_nrz(modulated_data: list[int]) -> list[int]:
    """
    Aplica a demodulação NRZ Polar aos dados modulados.\n
    Representa -1 como '0' e 1 como '1'.
    """
    return [0 if bit == -1 else 1 for bit in modulated_data]
