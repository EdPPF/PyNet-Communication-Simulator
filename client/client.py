import socket
import threading
import common.constants

from link_layer.framing.byte_insertion import byte_insertion
from link_layer.framing.char_count import char_count
from link_layer.error_detection.crc32 import append_crc32
from link_layer.error_detection.parity_bit import compute_parity_bit
from link_layer.error_correction.hamming import encode_hamming

from physical_layer.baseband_modulation.manchester import manchester
from physical_layer.baseband_modulation.nrz_polar import polar_nrz
from physical_layer.baseband_modulation.nrz_bipolar import bipolar_nrz
from physical_layer.carrier_modulation.ask import ask_modulation
from physical_layer.carrier_modulation.fsk import fsk_modulation
from physical_layer.carrier_modulation.qam8 import qam8_modulation


def process_message(message: str):
    # Modifica message para list[int] para aplicar enquadramento
    data = [ord(char) for char in message]

    # 1. Enquadramento
    while True:
        print("Escolha o protocolo de enquadramento:")
        for choice in ["1. Inserção de bytes", "2. Contagem de caracteres"]:
            print(f"{choice}")
        framing_choice = int(input("-> "))
        if framing_choice == 1:
            framed_message = byte_insertion(data)
            framing_protocol = "byte_insertion"
            break
        elif framing_choice == 2:
            framed_message = char_count(data)
            framing_protocol = "char_count"
            break
        else:
            print("Escolha inválida. Por favor, escolha novamente.")

    # 2. Detecção de erros
    while True:
        print("Escolha o protocolo de detecção de erros:")
        for choice in ["1. Bit de paridade", "2. CRC-32"]:
            print(f"{choice}")
        error_detection_choice = int(input("-> "))
        if error_detection_choice == 1:
            error_detection_protocol = "parity_bit"
            error_checked_message = compute_parity_bit(framed_message)
            break
        elif error_detection_choice == 2:
            error_detection_protocol = "crc32"
            error_checked_message = append_crc32(framed_message)
            break
        else:
            print("Escolha inválida. Por favor, escolha novamente.")
    # error_checked_message: list[int]
    print(f"error_checked_message: {error_checked_message}")

    # 3. Correção de erros - Hamming(7,4)
    encoded_message = encode_hamming(error_checked_message)
    # encoded_message: list[int]

    # 4. Modulação Banda Base
    while True:
        print("Escolha o protocolo de modulação banda base:")
        for choice in ["1. NRZ Polar", "2. NRZ Bipolar", "3. Manchester"]:
            print(f"{choice}")
        baseband_choice = int(input("-> "))
        if baseband_choice == 1:
            modulated_message = polar_nrz(encoded_message)
            baseband_protocol = "polar_nrz"
            break
        elif baseband_choice == 2:
            modulated_message = bipolar_nrz(encoded_message)
            baseband_protocol = "bipolar_nrz"
            break
        elif baseband_choice == 3:
            modulated_message = manchester(encoded_message)
            baseband_protocol = "manchester"
            break
        else:
            print("Escolha inválida. Por favor, escolha novamente.")

    # 5. Modulação de Portadora
    freq0 = 0
    freq1 = 0
    while True:
        print("Escolha o protocolo de modulação de portadora:")
        for choice in ["1. ASK", "2. FSK", "3. QAM-8"]:
            print(f"{choice}")
        carrier_choice = int(input("-> "))
        if carrier_choice == 1:
            amplitude = float(input("Digite a amplitude da onda portadora: "))
            frequency = float(input("Digite a frequência da onda portadora: "))
            modulated_message = ask_modulation(modulated_message, amplitude, frequency)
            carrier_protocol = "ask"
            break
        elif carrier_choice == 2:
            amplitude = float(input("Digite a amplitude da onda portadora: "))
            freq0 = float(input("Digite a frequência da onda portadora para '0': "))
            freq1 = float(input("Digite a frequência da onda portadora para '1': "))
            modulated_message = fsk_modulation(modulated_message, amplitude, freq0, freq1)
            carrier_protocol = "fsk"
            break
        elif carrier_choice == 3:
            amplitude = float(input("Digite a amplitude da onda portadora: "))
            frequency = float(input("Digite a frequência da onda portadora: "))
            modulated_message = qam8_modulation(modulated_message, amplitude, frequency)
            carrier_protocol = "qam8"
            break
        else:
            print("Escolha inválida. Por favor, escolha novamente.")

    # Retorna a mensagem modulada e a configuração de protocolos
    protocol_config = {
        "framing": framing_protocol,
        "error_detection": error_detection_protocol,
        "baseband": baseband_protocol,
        "carrier": carrier_protocol,
        "threshold": 0.5,  # Valor de limiar para ASK e FSK
        "amplitude": amplitude,  # Amplitude para QAM-8
        "f0": freq0,  # Frequência para '0' em FSK
        "f1": freq1,  # Frequência para '1' em FSK
    }
    return modulated_message, protocol_config


def start(host=common.constants.Host, port=common.constants.Port):
    """Inicia o cliente para enviar mensagens a um servidor."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))
        print(f"[INFO] Conectado a {host}:{port}")

        while True:
            message = input("Digite uma mensagem ou 'sair' para encerrar: ")
            if message.lower() == "sair":
                print("[INFO] Encerrando cliente.")
                break

            # Processa a mensagem com os protocolos
            processed_message, protocol_config = process_message(message)
            # Envia mensagem ao servidor
            client.sendall(str((processed_message, protocol_config)).encode())

            # Recebe resposta do servidor
            response = client.recv(1024).decode()
            print(f"Resposta do servidor: {response}")
    except Exception as e:
            print(f"[ERROR] {e}")
    finally:
        client.close()
        print("[INFO] Cliente encerrado.")

if __name__ == "__main__":
    start()
