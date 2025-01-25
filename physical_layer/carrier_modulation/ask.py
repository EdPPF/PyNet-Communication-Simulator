import math

def ask_modulation(data: list[int], amplitude: float, frequency: float) -> list[float]:
    """
    Aplica a modulação ASK nos dados.\n
    Para '1', gera um sinal senoidal com amplitude especificada.\n
    Para '0', gera um sinal nulo.
    """
    samples_per_bit = 100  # Número de pontos para amostrar cada bit
    modulated_signal = []

    for bit in data:
        if bit == 1:
            modulated_signal.extend(
                [amplitude * math.sin(2 * math.pi * frequency * t / samples_per_bit)
                 for t in range(samples_per_bit)]
            )
        else:
            modulated_signal.extend([0] * samples_per_bit)

    return modulated_signal

def ask_demodulation(modulated_signal: list[float], threshold: float) -> list[int]:
    """
    Demodula um sinal ASK.\n
    Se a média dos valores absolutos for maior que o threshold, é interpretado como '1', senão como '0'.
    """
    samples_per_bit = 100
    demodulated_data = []

    for i in range(0, len(modulated_signal), samples_per_bit):
        segment = modulated_signal[i:i + samples_per_bit]
        avg_amplitude = sum(abs(value) for value in segment) / samples_per_bit
        demodulated_data.append(1 if avg_amplitude > threshold else 0)

    return demodulated_data
