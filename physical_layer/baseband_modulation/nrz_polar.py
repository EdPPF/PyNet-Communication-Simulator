"""Modulação banda base por NRZ Polar."""

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


def main():
    # Valores pós workflow até hamming
    Original_Data = [2, 104, 105, 3, 0, 0, 0, 0] # hi + byte insertion + crc32
    Binary_Data   = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Hamming_Data  = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Length        = 112

    modulated_data = polar_nrz(Hamming_Data)
    print(f"Dados modulados: {modulated_data}\nLength: {len(modulated_data)}")

    demodulated_data = demodulate_polar_nrz(modulated_data)
    print(f"Dados demodulados: {demodulated_data}")

if __name__ == "__main__":
    main()
