import socket
import threading
import common.constants
from common.conversions import bytes_to_bits, bits_to_bytes, bytes_to_str

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
            # Recebe a quantidade de partes
            num_parts = int(client_socket.recv(1024).decode())
            print(f"[INFO] Quantidade de partes chegando: {num_parts}")
            received_parts = []

            for _ in range(num_parts):
            # Recebe mensagem do cliente
                message = client_socket.recv(8192).decode()
                if not message:
                    break

                modulated_data, protocol_config = eval(message) # Deserializa a mensagem
                # modulated_data: list[float]

                ''' Testando sem modulação por portadora
                # 1. Undo modulação de portadora
                if protocol_config["carrier"] == "ask":
                    baseband_data = ask_demodulation(modulated_data, protocol_config["threshold"])
                elif protocol_config["carrier"] == "fsk":
                    baseband_data = fsk_demodulation(modulated_data, protocol_config["f0"], protocol_config["f1"], protocol_config["threshold"])
                elif protocol_config["carrier"] == "qam8":
                    baseband_data = qam8_demodulation(modulated_data, protocol_config["amplitude"])
                '''

                baseband_data = modulated_data
                # 2. Undo modulação de banda base
                if protocol_config["baseband"] == "polar_nrz":
                    data = demodulate_polar_nrz(baseband_data)
                elif protocol_config["baseband"] == "bipolar_nrz":
                    data = demodulate_bipolar_nrz(baseband_data)
                elif protocol_config["baseband"] == "manchester":
                    data = demodulate_manchester(baseband_data)
                # data: list[int] de 0, 1 e -1

                # 3. Desfaz Hamming
                error_checked_message = decode_hamming(data)
                # error_checked_message: list[int]

                error_checked_message = bits_to_bytes(error_checked_message)

                # 4. Verifica detecção de erros
                if protocol_config["error_detection"] == "parity_bit":
                    verified, is_valid = verify_parity_bit(error_checked_message)
                elif protocol_config["error_detection"] == "crc32":
                    verified, is_valid = verify_crc32(error_checked_message)
                if not verified:
                    print("[ERROR] Erro detectado na mensagem recebida.")
                    client_socket.send("Erro detectado na mensagem recebida.".encode("utf-8"))
                    continue
                if not is_valid:
                    print("[ERROR] Mensagem corrompida.")
                    client_socket.send("Mensagem corrompida.".encode("utf-8"))
                    continue
                # verified: list[int]

                # print(f"PÓS HAMMING: {error_checked_message}")
                # print(f"VERIFIED: {verified}")
                # 5. Desfaz enquadramento
                if protocol_config["framing"] == "byte_insertion":
                    message = byte_removal(verified)
                elif protocol_config["framing"] == "char_count":
                    message = char_remove(verified)

                # Converte a mensagem para string
                message = bytes_to_str(message)
                print(f"Parte recebida de {address}: {message}")
                # Adiciona a parte recebida à lista de partes
                received_parts.append(message)
                # Envia resposta ao cliente
                client_socket.send("Parte recebida!\n".encode("utf-8"))
            # Envia confirmação final ao cliente
            client_socket.send("Todos os quadros recebidos.".encode("utf-8"))
            print(f"[INFO] Todas as partes recebidas de {address}")
            # Junta as partes na mensagem completa
            full_message = ""
            for part in received_parts:
                full_message += part
            print(f"Mensagem completa de {address}: {full_message}")
            break
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
