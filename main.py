"""
Permite o usuário selecionar entre iniciar o Cliente ou o Servidor.\n
O Cliente envia uma mensagem ao Servidor, que a devolve de volta.\n
Invoca a função main() do Cliente ou do Servidor, dependendo da escolha do usuário.
"""

def main():
    print("Selecione uma opção:")
    print("1 - Iniciar Servidor")
    print("2 - Iniciar Cliente")
    option = input("Opção: ")

    if option == "1":
        from server.server import main as server_main
        server_main()
    elif option == "2":
        from client.client import main as client_main
        client_main()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
