"""Constantes compartilhadas. Uso livre!"""

CRC32_POLYNOMIAL = 0x04C11DB7 # IEEE 802 CRC-32 polynomial
reverse_CRC_polynomial = 0xEDB88320

Host = "localhost"
Port = "8080"
Type = "tcp"

# ASCII Constants for framing
STX = 0x02 # Start of Text
ETX = 0x03 # End of Text
ESC = 0x1B # Escape
