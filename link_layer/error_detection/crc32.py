"""Protocolo de detcção de erro por CRC32."""

# import common.constants

# CRC32 precomputed table (used for faster computation)
CRC32_TABLE = [0]*256

def init():
    """Precomputes the CRC32 table using the polynomial 0x04C11DB7 (non-reflected)."""
    global CRC32_TABLE
    polynomial = 0x04C11DB7 # common.constants.CRC32_POLYNOMIAL
    for i in range(256):
        crc = i << 24  # Start with the byte in the most significant position
        for _ in range(8):
            if crc & 0x80000000:  # Check if the MSB is set
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
        CRC32_TABLE.append(crc & 0xFFFFFFFF)  # Limit to 32 bits

def compute_crc32(data: bytes) -> int:
    """Calculates the CRC32 checksum for a sequence of bytes."""
    global CRC32_TABLE
    if CRC32_TABLE == []:
        init()

    crc = 0xFFFFFFFF  # Initialize CRC with all bits set according to IEEE 802.3
    for byte in data:
        table_index = ((crc >> 24) ^ byte) & 0xFF  # Index into the CRC32 table. Usa o byte mais significativo
        crc = (crc << 8) ^ CRC32_TABLE[table_index]
    return crc & 0xFFFFFFFF

def append_crc32(data: list[int]) -> list[int]:
    """Appends the CRC32 checksum to the data."""
    # Converte a lista de int para bytes
    datab = bytes(data)
    crc = compute_crc32(datab)
    crc_bytes = list(crc.to_bytes(4, byteorder='big'))  # Convert CRC to 4 bytes in big-endian order
    return list(datab) + crc_bytes # Append the CRC bytes to the data

def verify_crc32(dataWithCRC: list[int]) -> tuple[list[int], bool]:
    """Verifies if the CRC32 checksum in the data is correct."""
    # Converte para bytes
    if len(dataWithCRC) < 4:
        return False  # Not enough data to include a CRC
    dataWithCRCBytes = bytes(dataWithCRC)
    data = dataWithCRCBytes[:-4]  # Extract original data (excluding the last 4 CRC bytes)
    received_crc = int.from_bytes(dataWithCRCBytes[-4:], byteorder='big')  # Extract CRC
    computed_crc = compute_crc32(data)
    # Verifica se o CRC recebido corresponde ao recalculado
    is_valid = (received_crc == computed_crc)
    # Converte os dados originais de volta para list[int]
    data_list = list(data)
    return data_list, is_valid


def main():
    message = "hi" # [2, 104, 105, 3] por byte insertion
    data = [2, 104, 105, 3]
    print(f"Original Data: {data}")
    framed_data = append_crc32(data)
    print(f"Framed Data  : {framed_data}")

    data, is_valid = verify_crc32(framed_data)
    print(f"Unframed Data: {data}")
    message = "".join([chr(byte) for byte in data])
    print(f"Message      : {message}")
    print(f"Is Valid     : {is_valid}")


if __name__ == "__main__":
    main()
