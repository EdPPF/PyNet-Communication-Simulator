"""Modulação por portadora QAM-8 (Quadrature Amplitude Modulation)."""

import math

def qam8_modulation(data: list[int], amplitude: float, frequency: float) -> list[tuple[float, float]]:
    """
    Aplica modulação QAM-8 nos dados.
    Cada três bits geram um símbolo de amplitude e fase.
    """
    if len(data) % 3 != 0:
        raise ValueError("A entrada precisa ter múltiplos de 3 bits para QAM-8.")

    samples_per_symbol = 100
    modulated_signal = []

    # Tabela de mapeamento para QAM-8
    qam_map = {
        (0, 0, 0): (amplitude / 2, 0),
        (0, 0, 1): (amplitude / 2, math.pi / 4),
        (0, 1, 0): (amplitude / 2, math.pi / 2),
        (0, 1, 1): (amplitude, 0),
        (1, 0, 0): (amplitude, math.pi / 4),
        (1, 0, 1): (amplitude, math.pi / 2),
        (1, 1, 0): (amplitude, 3 * math.pi / 4),
        (1, 1, 1): (amplitude, math.pi),
    }

    for i in range(0, len(data), 3):
        symbol = tuple(data[i:i + 3])
        amp, phase = qam_map[symbol]

        modulated_signal.extend(
            [amp * math.sin(2 * math.pi * frequency * t / samples_per_symbol + phase)
             for t in range(samples_per_symbol)]
        )

    return modulated_signal

def qam8_demodulation(modulated_signal: list[float], amplitude: float) -> list[int]:
    """
    Demodula um sinal QAM-8.\n
    Analisa amplitude e fase para identificar os três bits originais.
    """
    samples_per_symbol = 100
    num_symbols = len(modulated_signal) // samples_per_symbol
    demodulated_bits = []

    # Tabela de mapeamento inverso para QAM-8
    qam_map = {
        (amplitude / 2, 0): [0, 0, 0],
        (amplitude / 2, math.pi / 4): [0, 0, 1],
        (amplitude / 2, math.pi / 2): [0, 1, 0],
        (amplitude, 0): [0, 1, 1],
        (amplitude, math.pi / 4): [1, 0, 0],
        (amplitude, math.pi / 2): [1, 0, 1],
        (amplitude, 3 * math.pi / 4): [1, 1, 0],
        (amplitude, math.pi): [1, 1, 1],
    }

    for i in range(num_symbols):
        # Extrai os valores de amplitude e fase do sinal
        segment = modulated_signal[i * samples_per_symbol:(i + 1) * samples_per_symbol]
        first_sample = segment[0]  # Amplitude do primeiro ponto do símbolo

        # Calcula fase aproximada com base no primeiro e segundo pontos
        second_sample = segment[1]  # Para aproximar a fase
        phase = math.atan2(second_sample, first_sample) % (2 * math.pi)

        # Ajusta a amplitude para o intervalo esperado
        amplitude_detected = math.sqrt(first_sample**2 + second_sample**2)

        # Arredonda para aproximar ao mapa de QAM
        amplitude_rounded = round(amplitude_detected / (amplitude / 2)) * (amplitude / 2)
        phase_rounded = min(qam_map.keys(), key=lambda key: abs(key[1] - phase))[1]

        # Busca no mapa de símbolos
        bits = qam_map.get((amplitude_rounded, phase_rounded), [0, 0, 0])
        demodulated_bits.extend(bits)

    return demodulated_bits
