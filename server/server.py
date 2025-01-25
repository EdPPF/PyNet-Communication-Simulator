import socket
import threading
import common.constants

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Data recebida: {bin(data)}")
            # Converte a mensagem de bytes para string
            message = data.decode("utf-8")
            print(f"Mensagem decodificada: {message}")
            # Devolve um 'ack' para o cliente
            client_socket.sendall("MENSAGEM RECEBIDA")
        except Exception as e:
            print(f"Erro recebendo mensagem do cliente: {e}")
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((common.constants.Host, common.constants.Port))
    server_socket.listen(5)
    print(f"Servidor escutando em {common.constants.Host}:{common.constants.Port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexão de {address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
