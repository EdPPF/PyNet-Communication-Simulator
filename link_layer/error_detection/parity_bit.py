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
