import socket
import threading
import common.constants
from common.conversions import bytes_to_bits, bits_to_bytes

from link_layer.framing.byte_insertion import byte_removal
from link_layer.framing.char_count import char_remove
from link_layer.error_detection.crc32 import verify_crc32
from link_layer.error_detection.parity_bit import verify_parity_bit
from link_layer.error_correction.hamming import decode_hamming

from physical_layer.baseband_modulation.manchester import demodulate_manchester
from physical_layer.baseband_modulation.nrz_polar import demodulate_polar_nrz
from physical_layer.baseband_modulation.nrz_bipolar import demodulate_bipolar_nrz
from physical_layer.carrier_modulation.ask import ask_demodulation
from physical_layer.carrier_modulation.fsk import fsk_demodulation
from physical_layer.carrier_modulation.qam8 import qam8_demodulation

def handle_client(client_socket, address):
    """Lida com comunicação com um cliente."""
    print(f"[INFO] Conexão estabelecida com {address}")
    try:
        while True:
            # Recebe mensagem do cliente
            message = client_socket.recv(4194304).decode()
            if not message:
                break
            print(f"Sinal recebido.")
            print(message)

            modulated_data, protocol_config = eval(message) # Deserializa a mensagem
            # modulated_data: list[float]

            # 1. Undo modulação de portadora
            if protocol_config["carrier"] == "ask":
                baseband_data = ask_demodulation(modulated_data, protocol_config["threshold"])
            elif protocol_config["carrier"] == "fsk":
                baseband_data = fsk_demodulation(modulated_data, protocol_config["f0"], protocol_config["f1"], protocol_config["threshold"])
            elif protocol_config["carrier"] == "qam8":
                baseband_data = qam8_demodulation(modulated_data, protocol_config["amplitude"])
            # baseband_data: list[int]

            # 2. Undo modulação de banda base
            if protocol_config["baseband"] == "polar_nrz":
                data = demodulate_polar_nrz(baseband_data)
            elif protocol_config["baseband"] == "bipolar_nrz":
                data = demodulate_bipolar_nrz(baseband_data)
            elif protocol_config["baseband"] == "manchester":
                data = demodulate_manchester(baseband_data)
            # data: list[int]

            # 3. Desfaz Hamming
            error_checked_message = decode_hamming(data)
            # error_checked_message: list[int]

            error_checked_message = bits_to_bytes(error_checked_message)

            # 4. Verifica detecção de erros
            if protocol_config["error_detection"] == "parity_bit":
                verified, is_valid = verify_parity_bit(error_checked_message)
            elif protocol_config["error_detection"] == "crc32":
                verified, is_valid = verify_crc32(error_checked_message)
                print("CRC32 OK")
            if not verified:
                print("[ERROR] Erro detectado na mensagem recebida.")
                client_socket.send("Erro detectado na mensagem recebida.".encode("utf-8"))
                continue
            if not is_valid:
                print("[ERROR] Mensagem corrompida.")
                client_socket.send("Mensagem corrompida.".encode("utf-8"))
                continue
            # verified: list[int]

            # 5. Desfaz enquadramento
            if protocol_config["framing"] == "byte_insertion":
                message = byte_removal(error_checked_message)
            elif protocol_config["framing"] == "char_count":
                message = char_remove(error_checked_message)
                print("Char Count OK")

            # TODO converter a mensagem para string
            # Imprime a mensagem recebida
            print(f"Mensagem recebida de {address}: {message}")

            # Envia resposta ao cliente
            client_socket.send("Mensagem recebida!".encode("utf-8"))
    except Exception as e:
        print(f"[ERROR] ao lidar com cliente: {e}")
        client_socket.send("Erro ao lidar com a mensagem.".encode("utf-8"))
    finally:
        print(f"[INFO] Conexão encerrada com {address}")
        client_socket.close()


def start(host=common.constants.Host, port=common.constants.Port):
    """Inicia o servidor para receber mensagens de clientes."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
        server.listen(5) # Aceita até 5 conexões pendentes
        print(f"[INFO] Servidor iniciado em {host}:{port}")
        print("[INFO] Aguardando conexões...")

        while True:
            client_socket, address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True # Encerra a thread quando o programa principal encerrar
            client_thread.start()
            print(f"[INFO] Thread iniciada para {address}.")
            print(f"[INFO] Total de conexões ativas: {threading.active_count() - 1}")
    except Exception as e:
        print(f"[ERROR] ao iniciar servidor: {e}")
    finally:
        server.close()
        print("[INFO] Servidor encerrado.")


if __name__ == "__main__":
    start()
