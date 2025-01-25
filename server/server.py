import socket
import threading
import common.constants

def handle_client(client_socket, address):
    """Lida com comunicação com um cliente."""
    print(f"[INFO] Conexão estabelecida com {address}")
    try:
        while True:
            # Recebe mensagem do cliente
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"Mensagem recebida de {address}: {message}")

            # TODO implementar pipeline dos protocolos (desenquadramento, detecção/correção de erros e demodulação)

            # Envia resposta ao cliente
            client_socket.send("Mensagem recebida!".encode("utf-8"))
    except Exception as e:
        print(f"[ERROR] {e}")
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

        while True:
            client_socket, address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True # Encerra a thread quando o programa principal encerrar
            client_thread.start()
            print(f"[INFO] Thread iniciada para {address}.")
            print(f"[INFO] Total de conexões ativas: {threading.active_count() - 1}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        server.close()
        print("[INFO] Servidor encerrado.")


if __name__ == "__main__":
    start()
