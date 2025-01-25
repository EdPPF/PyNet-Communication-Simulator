"""Protocolo de correção de erro por Hamming(7,4)."""

def encode_hamming(frame: list[int]) -> list[int]:
    """Encodes a frame using Hamming(7,4) and returns the encoded frame."""
    encoded = []
    for i in range(0, len(frame), 4):
        # Processa 4 bits por vez
        bits = frame[i:i+4]
        # Preenche com 0 se não houver 4 bits
        while len(bits) < 4:
            bits.append(0)
        # Aplica Hamming(7,4) e adiciona ao quadro codificado
        encoded += hamming_7_4(bits)
    return encoded

def hamming_7_4(bits: list[int]) -> list[int]:
    """Encodes 4 bits using Hamming(7,4)."""
    p1 = (bits[0] + bits[1] + bits[3]) % 2
    p2 = (bits[0] + bits[2] + bits[3]) % 2
    p3 = (bits[1] + bits[2] + bits[3]) % 2
    return [p1, p2, bits[0], p3, bits[1], bits[2], bits[3]]

def decode_hamming(frame: list[int]) -> list[int]:
    """
    Decodes a Hamming(7,4)-encoded frame and corrects errors if possible.\n
    Returns the decoded frame and a boolean indicating if an error was corrected.
    """
    # Converte a lista de inteiros em string binária
    frame_str = "".join(map(str, frame))
    decoded = ""
    for i in range(0, len(frame_str), 7):
        decoded += correct_hamming(frame_str[i:i+7])
        # Converte de volta em list[int]
    return [int(bit) for bit in decoded]

def correct_hamming(bits: str) -> str:
    """Corrects a single-bit error in a 7-bit Hamming frame."""
    p1 = (int(bits[0]) + int(bits[2]) + int(bits[4]) + int(bits[6])) % 2
    p2 = (int(bits[1]) + int(bits[2]) + int(bits[5]) + int(bits[6])) % 2
    p3 = (int(bits[3]) + int(bits[4]) + int(bits[5]) + int(bits[6])) % 2
    error_position = (p3 << 2) | (p2 << 1) | p1
    if error_position:
        # Correct the error
        error_index = 7 - error_position
        bits = bits[:error_index] + str(1 - int(bits[error_index])) + bits[error_index+1:]
    return bits[2] + bits[4:7]
