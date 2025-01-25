import socket
import common.constants

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

            # TODO implementat pipeline dos protocolos (enquadramento, detecção/correção de erros e modulação)

            # Envia mensagem ao servidor
            client.send(message.encode("utf-8"))

            # Recebe resposta do servidor
            response = client.recv(1024).decode("utf-8")
            print(f"Resposta do servidor: {response}")
    except Exception as e:
            print(f"[ERROR] {e}")
    finally:
        client.close()
        print("[INFO] Cliente encerrado.")

if __name__ == "__main__":
    start()
