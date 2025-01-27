import socket
import threading
import common.constants
from common.conversions import bytes_to_bits, bits_to_bytes, bytes_to_str
from link_layer.framing.byte_insertion import byte_removal
from link_layer.framing.char_count import char_remove
from link_layer.error_detection.crc32 import verify_crc32
from link_layer.error_detection.parity_bit import verify_parity_bit
from link_layer.error_correction.hamming import decode_hamming
from physical_layer.baseband_modulation.manchester import demodulate_manchester
from physical_layer.baseband_modulation.nrz_polar import demodulate_polar_nrz
from physical_layer.baseband_modulation.nrz_bipolar import demodulate_bipolar_nrz
from physical_layer.carrier_modulation.ask import ask_demodulation
from physical_layer.carrier_modulation.fsk import fsk_demodulation
from physical_layer.carrier_modulation.qam8 import qam8_demodulation
import tkinter as tk
from tkinter import ttk, scrolledtext

class ProtocolServer:
    def __init__(self, host=common.constants.Host, port=common.constants.Port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.root = None
        self.log_text = None
        self.active_connections = 0
        self.connection_label = None
        self.addresses = []

    def log_message(self, message):
        """Add message to the scrolled text widget"""
        if self.log_text:
            self.log_text.configure(state='normal')
            self.log_text.insert(tk.END, message + '\n')
            self.log_text.see(tk.END)
            self.log_text.configure(state='disabled')
            self.root.update()

    def update_connections_count(self):
        """Update the connection count label"""
        if self.connection_label:
            self.connection_label.config(
                text=f"Conexões ativas: {self.active_connections}")

    def handle_client(self, client_socket, address):
        while True:
            """Handle communication with a client."""
            
            if address not in self.addresses:
                self.addresses.append(address)
                self.active_connections += 1
                self.update_connections_count()
                self.log_message(f"[INFO] Conexão estabelecida com {address}")

            try:
                while True:
                    # Receive number of parts
                    num_parts = int(client_socket.recv(1024).decode())
                    self.log_message(f"[INFO] Quantidade de partes chegando: {num_parts}")
                    received_parts = []

                    for _ in range(num_parts):
                        message = client_socket.recv(1024).decode()
                        if not message:
                            break

                        modulated_data, protocol_config = eval(message)
                        data = modulated_data  # Currently testing without modulation

                        # 3. Undo Hamming
                        error_checked_message = decode_hamming(data)
                        error_checked_message = bits_to_bytes(error_checked_message)

                        # 4. Verify error detection
                        if protocol_config["error_detection"] == "parity_bit":
                            verified, is_valid = verify_parity_bit(error_checked_message)
                        elif protocol_config["error_detection"] == "crc32":
                            verified, is_valid = verify_crc32(error_checked_message)

                        if not verified:
                            self.log_message("[ERROR] Erro detectado na mensagem recebida.")
                            client_socket.send("Erro detectado na mensagem recebida.".encode("utf-8"))
                            continue
                        if not is_valid:
                            self.log_message("[ERROR] Mensagem corrompida.")
                            client_socket.send("Mensagem corrompida.".encode("utf-8"))
                            continue

                        # 5. Undo framing
                        if protocol_config["framing"] == "byte_insertion":
                            message = byte_removal(verified)
                        elif protocol_config["framing"] == "char_count":
                            message = char_remove(verified)

                        # Convert message to string
                        message = bytes_to_str(message)
                        self.log_message(f"Parte recebida de {address}: {message}")
                        received_parts.append(message)
                        client_socket.send("Parte recebida!".encode("utf-8"))

                    # Send final confirmation to client
                    client_socket.send("Todos os quadros recebidos.".encode("utf-8"))
                    self.log_message(f"[INFO] Todas as partes recebidas de {address}")
                    
                    # Join parts into complete message
                    full_message = "".join(received_parts)
                    self.log_message(f"Mensagem completa de {address}: {full_message}")
                    break

            except Exception as e:
                self.log_message(f"[INFO] Conexão com cliente encerrada")
                client_socket.send("Erro ao lidar com a mensagem.".encode("utf-8"))
                self.active_connections -= 1
                self.update_connections_count()
            finally:
                if full_message == "sair":
                    self.log_message(f"[INFO] Conexão encerrada com {address}")
                    client_socket.close()

    def setup_gui(self):
        """Setup the server GUI"""
        self.root = tk.Tk()
        self.root.title("SERVIDOR")
        self.root.geometry("600x400")

        # Server status frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=5, pady=5)

        # Status label
        status_label = ttk.Label(
            status_frame, 
            text=f"Servidor rodando em {self.host}:{self.port}")
        status_label.pack(side=tk.LEFT, padx=5)

        # Connection counter
        self.connection_label = ttk.Label(
            status_frame, 
            text="Conexões ativas: 0")
        self.connection_label.pack(side=tk.RIGHT, padx=5)

        # Log area
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrolled text widget for logs
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            wrap=tk.WORD, 
            height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state='disabled')

        # Stop button
        stop_button = ttk.Button(
            self.root, 
            text="Parar Servidor", 
            command=self.stop_server)
        stop_button.pack(pady=10)

    def stop_server(self):
        """Stop the server and close the window"""
        self.server.close()
        self.log_message("[INFO] Servidor encerrado.")
        self.root.quit()
        self.root.destroy()

    def start(self):
        """Start the server"""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            
            # Setup and start GUI
            self.setup_gui()
            
            # Start accepting connections in a separate thread
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            # Start GUI main loop
            self.root.mainloop()
            
        except Exception as e:
            if self.root:
                self.log_message(f"[ERROR] ao iniciar servidor: {e}")
            else:
                print(f"[ERROR] ao iniciar servidor: {e}")
        finally:
            self.server.close()

    def accept_connections(self):
        """Accept incoming connections"""
        while True:
            try:
                client_socket, address = self.server.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address))
                client_thread.daemon = True
                client_thread.start()
            except:
                break

def start(host=common.constants.Host, port=common.constants.Port):
    """Start the server"""
    server = ProtocolServer(host, port)
    server.start()

if __name__ == "__main__":
    start()