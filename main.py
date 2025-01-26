"""
Permite o usuário selecionar entre iniciar o Cliente ou o Servidor.\n
O Cliente envia uma mensagem ao Servidor, que a devolve de volta.\n
Invoca a função main() do Cliente ou do Servidor, dependendo da escolha do usuário.
"""

from server.server import start as start_server
from client.client import start as start_client

import tkinter as tk
from servidor_gui import exibir_segunda_janela
from cliente_gui import criar_janela_principal


def main():
    # print("Selecione uma opção:")
    # print("1 - Iniciar Servidor")
    # print("2 - Iniciar Cliente")
    # option = input("Opção: ")

    def iniciar_servidor():
        root.destroy()  # Fecha a janela principal
        start_server()  # Inicia o servidor

    def iniciar_cliente():
        root.destroy()  # Fecha a janela principal
        start_client()  # Inicia o cliente

    root = tk.Tk()
    root.title("Menu")
    root.geometry("300x200")

    tk.Label(root, text="Selecione uma opção:").pack(pady=10)

    tk.Button(root, text="1 - Iniciar Servidor", command=iniciar_servidor).pack(pady=10)
    tk.Button(root, text="2 - Iniciar Cliente", command=iniciar_cliente).pack(pady=10)

    root.mainloop()

    # if option == "1":
    #     start_server()
    # elif option == "2":
    #     start_client()
    # else:
    #     print("Opção inválida.")

if __name__ == "__main__":
    main()
