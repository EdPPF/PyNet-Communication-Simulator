import common.constants

# CRC32 precomputed table (used for faster computation)
_crc32_table = None

def init():
    """Precomputes the CRC32 table using the polynomial 0x04C11DB7 (non-reflected)."""
    global CRC32_TABLE
    polynomial = common.constants.CRC32_POLYNOMIAL
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
    global _crc32_table
    if _crc32_table is None:
        init()

    crc = 0xFFFFFFFF  # Initialize CRC with all bits set according to IEEE 802.3
    for byte in data:
        table_index = ((crc >> 24) ^ byte) & 0xFF  # Index into the CRC32 table. Usa o byte mais significativo
        crc = (crc << 8) ^ _crc32_table[table_index]
    return crc & 0xFFFFFFFF

def append_crc32(data: bytes):
    """Appends the CRC32 checksum to the data."""
    crc = compute_crc32(data)
    crc_bytes = crc.to_bytes(4, byteorder='big')  # Convert CRC to 4 bytes in big-endian order
    return data + list(crc_bytes) # Append the CRC bytes to the data

def verify_crc32(dataWithCRC: bytes) -> bool:
    """Verifies if the CRC32 checksum in the data is correct."""
    if len(dataWithCRC) < 4:
        return False  # Not enough data to include a CRC
    data = dataWithCRC[:-4]  # Extract original data (excluding the last 4 CRC bytes)
    received_crc = int.from_bytes(dataWithCRC[-4:], byteorder='big')  # Extract CRC
    computed_crc = compute_crc32(data)
    return data, computed_crc == received_crc
