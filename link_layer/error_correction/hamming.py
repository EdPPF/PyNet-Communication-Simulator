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
    # frame_str = "".join(map(str, frame))
    decoded = []
    for i in range(0, len(frame), 7):
        decoded += correct_hamming(frame[i:i+7])
    # Converte de volta em list[int]
    # return [int(bit) for bit in decoded]
    return decoded

def correct_hamming(bits: list[int]) -> list[int]:
    """Corrects a single-bit error in a 7-bit Hamming frame."""
    p1 = (bits[0] + bits[2] + bits[4] + bits[6]) % 2
    p2 = (bits[1] + bits[2] + bits[5] + bits[6]) % 2
    p3 = (bits[3] + bits[4] + bits[5] + bits[6]) % 2
    error_position = (p3 << 2) | (p2 << 1) | p1
    if error_position:
        # Correct the error
        error_index = 7 - error_position
        bits = bits[:error_index] + (1 - bits[error_index]) + bits[error_index+1:]
    return [bits[2]] + bits[4:7]


def main():
    def bytes_to_bits(byte_array):
        bits = []
        for byte in byte_array:
            # Convert byte to binary and fill with leading zeros to ensure 8 bits
            binary_representation = f'{byte:08b}'
            # Extend the bits list with the bits from the binary representation
            bits.extend(int(bit) for bit in binary_representation)
        return bits

    def bits_to_bytes(bit_array):
        bytes_array = []
        # Process the bits in chunks of 8
        for i in range(0, len(bit_array), 8):
            byte = 0
            # Construct the byte from the 8 bits
            for bit in bit_array[i:i + 8]:
                byte = (byte << 1) | bit  # Shift left and add the bit
            bytes_array.append(byte)
        return bytes_array


    message = "hi" # [2, 104, 105, 3, 0, 0, 0, 0] por byte insertion + crc32
    data = [2, 104, 105, 3, 0, 0, 0, 0]
    # Transforma a lista de ASCII em uma lista de bits.
    # Ex.: [104, 105] -> [0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1]
    datab = bytes_to_bits(data)
    print(f"Original Data : {data} (hi)")
    print(f"Binary Data   : {datab}")
    hamming_data = encode_hamming(datab)
    print(f"Hamming Data  : {hamming_data}")
    print(f"Length        : {len(hamming_data)}")

    data = decode_hamming(hamming_data)
    print(f"Unhamming Data: {data}")
    databy = bits_to_bytes(data)
    message = "".join([chr(byte) for byte in databy])
    print(f"Message       : {message}")


if __name__ == "__main__":
    main()
