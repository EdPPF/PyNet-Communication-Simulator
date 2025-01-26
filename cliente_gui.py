import tkinter as tk
from servidor_gui import exibir_segunda_janela  # Importa a função da outra janela

def criar_janela_principal():
    # Criação da janela principal
    root = tk.Tk()
    root.title("CLIENTE")

    # Criação do campo de entrada de texto

    entry_label = tk.Label(root, text="Digite uma mensagem ou 'sair' para encerrar: ")
    entry_label.pack(pady=10)

    entry = tk.Entry(root)
    entry.pack(pady=10)

    # Função que é chamada quando o botão "Enviar" é pressionado
    def enviar_dados():
        dado = entry.get()  # Pega o dado digitado
        return dado
        #exibir_segunda_janela(dado)  # Chama a função que exibe a segunda janela

    # Criação do botão "Enviar"
    button = tk.Button(root, text="Enviar", command=enviar_dados)
    button.pack(pady=20)
    
    # Iniciar o loop da interface gráfica
    root.mainloop()
def fechar_janela(): 
    root.destroy()