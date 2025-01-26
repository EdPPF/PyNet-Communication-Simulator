import tkinter as tk
from servidor_gui import exibir_segunda_janela  # Importa a função da outra janela

def criar_janela_principal():
    # Criação da janela principal
    root = tk.Tk()
    root.title("CLIENTE")

    # Criação do campo de entrada de texto

    
    # Iniciar o loop da interface gráfica
    #root.mainloop()
    return root

def fechar_janela(root): 
    root.destroy()

def enviar_dados(root):
    dado = tk.StringVar()  # Variável especial do Tkinter

    entry_label = tk.Label(root, text="Digite uma mensagem ou 'sair' para encerrar: ")
    entry_label.pack(pady=10) 

    caixa_texto = tk.Entry(root, width=30)
    caixa_texto.pack(pady=10)

    def pegar_texto():
        texto=caixa_texto.get()
        return texto
    

    # Botão para enviar os dados
    button = tk.Button(root, text="Enviar", command=pegar_texto)
    button.pack(pady=20)
    return pegar_texto

