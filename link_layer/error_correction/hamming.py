def encode_hamming(frame: str) -> str:
    """Encodes a frame using Hamming(7,4) and returns the encoded frame."""
    encoded = ""
    for char in frame:
        bits = f"{ord(char):08b}"  # Convert char to 8-bit binary
        encoded += hamming_7_4(bits[:4]) + hamming_7_4(bits[4:])
    return encoded

def hamming_7_4(bits: str) -> str:
    """Encodes 4 bits using Hamming(7,4)."""
    p1 = (int(bits[0]) + int(bits[1]) + int(bits[3])) % 2
    p2 = (int(bits[0]) + int(bits[2]) + int(bits[3])) % 2
    p3 = (int(bits[1]) + int(bits[2]) + int(bits[3])) % 2
    return f"{p1}{p2}{bits[0]}{p3}{bits[1:]}"

def decode_hamming(frame: str) -> str:
    """Decodes a Hamming(7,4)-encoded frame and corrects errors if possible."""
    decoded = ""
    for i in range(0, len(frame), 7):
        decoded += correct_hamming(frame[i:i+7])
    return decoded

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
