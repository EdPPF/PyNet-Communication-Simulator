"""Protocolo de detecção de erro por bit de paridade PAR."""

def compute_parity_bit(frame: list[int]) -> list[int]:
    """Calcula o bit de paridade em um frame e o adiciona."""
    parity = sum(frame) % 2
    frame.append(parity)
    return frame

def verify_parity_bit(frame: list[int]) -> tuple[list[int], bool]:
    """Verifica se o bit de paridade em um frame está correto."""
    # Verifica o último bit (bit de paridade)
    data = frame[:-1]
    parity_bit = frame[-1]

    # Calcula a paridade dos bits de dados
    computed_parity = sum(bit for bit in data) % 2

    # Verifica se a paridade calculada corresponde ao bit de paridade
    is_valid = (computed_parity == parity_bit)

    return data, is_valid


def main():
    message = "hi" # [2, 104, 105, 3] por byte insertion
    data = [2, 104, 105, 3]
    print(f"Original Data: {data}")
    framed_data = compute_parity_bit(data)
    print(f"Framed Data  : {framed_data}")

    data, is_valid = verify_parity_bit(framed_data)
    print(f"Unframed Data: {data}")
    message = "".join([chr(byte) for byte in data])
    print(f"Message      : {message}")
    print(f"Is Valid     : {is_valid}")

if __name__ == "__main__":
    main()
