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

def bytes_to_bits(byte_array):
    bits = []
    for byte in byte_array:
        # Convert byte to binary and fill with leading zeros to ensure 8 bits
        binary_representation = f'{byte:08b}'
        # Extend the bits list with the bits from the binary representation
        bits.extend(int(bit) for bit in binary_representation)
    return bits
