"""Protocolo de enquadramento por inserção de bytes."""

import common.constants

ESC = common.constants.ESC
STX = common.constants.STX
ETX = common.constants.ETX

def byte_insertion(data: list[int]) -> list[int]:
    """Aplica Byte Insertion em uma sequência de bytes.\n
    Adiciona bytes especiais no início e fim da mensagem, escapando bytes especiais."""
    framed_data = [STX]  # Adiciona o byte de início de texto
    for byte in data:
        if byte in (ESC, STX, ETX):
            framed_data.append(ESC) # Adiciona o byte de escape
        framed_data.append(byte)
    framed_data.append(ETX)  # Adiciona o byte de fim de texto
    return framed_data

def byte_removal(framed_data: list[int]) -> list[int]:
    """Remove os bytes especiais de uma sequência de bytes."""
    if framed_data[0] != STX or framed_data[-1] != ETX:
        raise ValueError("Quadro inválido: não começa ou termina com STX e ETX.")

    data = []
    escape_next = False
    for byte in framed_data[1:-1]:  # Ignora os bytes de início e fim de texto
        if escape_next:
            data.append(byte)
            escape_next = False
        elif byte == ESC:
            escape_next = True
        else:
            data.append(byte)
    return data
