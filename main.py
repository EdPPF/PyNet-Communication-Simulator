"""
Permite o usuário selecionar entre iniciar o Cliente ou o Servidor.\n
O Cliente envia uma mensagem ao Servidor, que a devolve de volta.\n
Invoca a função main() do Cliente ou do Servidor, dependendo da escolha do usuário.
"""

from server.server import start as start_server
from client.client import start as start_client


def main():
    print("Selecione uma opção:")
    print("1 - Iniciar Servidor")
    print("2 - Iniciar Cliente")
    option = input("Opção: ")

    if option == "1":
        start_server()
    elif option == "2":
        start_client()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
