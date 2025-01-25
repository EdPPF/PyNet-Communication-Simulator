def compute_parity_bit(frame: str) -> str:
    """Calcula o bit de paridade em um frame e o adicioa."""
    parity = sum(1 for bit in frame if bit == "1") % 2
    return frame + ('1' if parity == 1 else '0')

def verify_parity_bit(frame: str) -> bool:
    """Verifica se o bit de paridade em um frame está correto."""
    parity = sum(1 for bit in frame[:-1] if bit == "1") % 2
    return parity == int(frame[-1])
