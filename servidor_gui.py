import tkinter as tk

def exibir_segunda_janela():
    root = tk.Tk()
    root.title("SERVIDOR")
   
    # Exibe o dado recebido na nova janela
    # label = tk.Label(segunda_janela, text=f"Dado recebido: {dado}")
    # label.pack(pady=10)

    print("before main loop")
    root.mainloop()
    print("after main loop")
