import math

def fsk_modulation(data: list[int], amplitude: float, freq0: float, freq1: float) -> list[float]:
    """
    Aplica a modulação FSK nos dados.\n
    Para '0', utiliza uma frequência `freq0`.\n
    Para '1', utiliza uma frequência `freq1`.
    """
    samples_per_bit = 100
    modulated_signal = []

    for bit in data:
        frequency = freq1 if bit == 1 else freq0
        modulated_signal.extend(
            [amplitude * math.sin(2 * math.pi * frequency * t / samples_per_bit)
             for t in range(samples_per_bit)]
        )

    return modulated_signal

def fsk_demodulation(modulated_signal: list[float], freq0: float, freq1: float, threshold: float) -> list[int]:
    """
    Demodula um sinal FSK.\n
    Calcula a energia em cada segmento para determinar se corresponde a freq0 ou freq1.
    """
    samples_per_bit = 100
    demodulated_data = []

    for i in range(0, len(modulated_signal), samples_per_bit):
        segment = modulated_signal[i:i + samples_per_bit]

        # Energia para freq0
        energy0 = sum(
            (value - math.sin(2 * math.pi * freq0 * t / samples_per_bit))**2
            for t, value in enumerate(segment)
        )

        # Energia para freq1
        energy1 = sum(
            (value - math.sin(2 * math.pi * freq1 * t / samples_per_bit))**2
            for t, value in enumerate(segment)
        )

        # Decide qual frequência predomina
        demodulated_data.append(1 if energy1 < energy0 else 0)

    return demodulated_data
