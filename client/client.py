import socket
import threading
from link_layer import *
import common.constants#.{Host, Port, Type}

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received: {message}")
        except:
            print("CUUUUUUUUU")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((common.constants.Host, common.constants.Port))

    threading.Thread(target=receive_message, args=(client_socket,)).start()

    while True:
        message = input("Digite uma mensagem ou 'exit' para sair: ")
        if message == "exit":
            break
        data = [ord(char) for char in message] # Convertendo a mensagem para uma lista de inteiros
        # Transforma em bytes
        data = bytes(data)
        client_socket.sendall(data)

    client_socket.close()

if __name__ == "__main__":
    main()
