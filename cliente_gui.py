import tkinter as tk
from typing import Callable

class ClientGUI:
    def __init__(self, message_callback: Callable[[str], None]):
        self.root = tk.Tk()
        self.root.title("CLIENTE")
        self.message_callback = message_callback
        self.setup_gui()

    def setup_gui(self):
        # Entry label
        entry_label = tk.Label(self.root, text="Digite uma mensagem ou 'sair' para encerrar: ")
        entry_label.pack(pady=10)

        # Entry field
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=10)
        
        # Send button
        button = tk.Button(self.root, text="Enviar", command=self.enviar_dados)
        button.pack(pady=20)

        # Bind Enter key to send message
        self.entry.bind('<Return>', lambda event: self.enviar_dados())

    def enviar_dados(self):
        dado = self.entry.get()  # Get the entered text
        self.entry.delete(0, tk.END)  # Clear the entry field
        if self.message_callback:
            self.message_callback(dado)  # Call the callback function with the message
        
        if dado.lower() == 'sair':
            self.root.quit()

    def start(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()