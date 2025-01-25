def char_count(frame: list[int])-> list[int]:
    """Conta o número de caracteres em uma mensagem e adiciona no início da mensagem."""
    if len(frame) > 255:
        raise ValueError("Mensagem muito grande para ser contada.")
    return [len(frame)] + frame

def char_remove(frame: list[int]) -> list[int]:
    """Remove o número de caracteres no início da mensagem."""
    if len(frame) == 0:
        raise ValueError("Quadro vazio.")
    char_counted = frame[0]
    if len(frame[1:]) != char_counted:
        raise ValueError("Erro no quadro: Número de caracteres não corresponde ao tamanho do quadro.")
    return frame[1:]
