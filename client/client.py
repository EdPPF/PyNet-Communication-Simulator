import socket
import threading
import common.constants
from common.conversions import bytes_to_bits, bits_to_bytes
from link_layer.framing.byte_insertion import byte_insertion
from link_layer.framing.char_count import char_count
from link_layer.error_detection.crc32 import append_crc32
from link_layer.error_detection.parity_bit import compute_parity_bit
from link_layer.error_correction.hamming import encode_hamming
from physical_layer.baseband_modulation.manchester import manchester
from physical_layer.baseband_modulation.nrz_polar import polar_nrz
from physical_layer.baseband_modulation.nrz_bipolar import bipolar_nrz
from physical_layer.carrier_modulation.ask import ask_modulation
from physical_layer.carrier_modulation.fsk import fsk_modulation
from physical_layer.carrier_modulation.qam8 import qam8_modulation
import tkinter as tk
from tkinter import ttk
from cliente_gui import ClientGUI

class ProtocolClient:
    def __init__(self, host=common.constants.Host, port=common.constants.Port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gui = None
        self.protocol_window = None
        self.info_label = None
        self.protocol_vars = {}  # We'll initialize these when creating the protocol window
        self.params_frame = None

    def fragment_message(self, message: str, frame_size: int) -> list[str]:
        return [message[i:i + frame_size] for i in range(0, len(message), frame_size)]

    def create_protocol_window(self):
        self.protocol_window = tk.Toplevel()
        self.protocol_window.title("Protocol Configuration")
        
        # Initialize protocol variables here, after creating the window
        self.protocol_vars = {
            'framing': tk.StringVar(self.protocol_window),
            'error_detection': tk.StringVar(self.protocol_window),
            'baseband': tk.StringVar(self.protocol_window),
            'carrier': tk.StringVar(self.protocol_window),
            'amplitude': tk.StringVar(self.protocol_window),
            'frequency': tk.StringVar(self.protocol_window),
            'freq0': tk.StringVar(self.protocol_window),
            'freq1': tk.StringVar(self.protocol_window)
        }

        # Set default values
        self.protocol_vars['framing'].set("byte_insertion")
        self.protocol_vars['error_detection'].set("parity_bit")
        self.protocol_vars['baseband'].set("polar_nrz")
        self.protocol_vars['carrier'].set("ask")
        
        # Framing
        frame_label = tk.Label(self.protocol_window, text="Escolha o protocolo de enquadramento:")
        frame_label.pack(pady=5)
        frame_frame = ttk.Frame(self.protocol_window)
        frame_frame.pack(pady=5)
        ttk.Radiobutton(frame_frame, text="Inserção de bytes", variable=self.protocol_vars['framing'], 
                       value="byte_insertion").pack()
        ttk.Radiobutton(frame_frame, text="Contagem de caracteres", variable=self.protocol_vars['framing'], 
                       value="char_count").pack()

        # Error Detection
        error_label = tk.Label(self.protocol_window, text="Escolha o protocolo de detecção de erros:")
        error_label.pack(pady=5)
        error_frame = ttk.Frame(self.protocol_window)
        error_frame.pack(pady=5)
        ttk.Radiobutton(error_frame, text="Bit de paridade", variable=self.protocol_vars['error_detection'], 
                       value="parity_bit").pack()
        ttk.Radiobutton(error_frame, text="CRC-32", variable=self.protocol_vars['error_detection'], 
                       value="crc32").pack()

        # Baseband Modulation
        baseband_label = tk.Label(self.protocol_window, text="Escolha o protocolo de modulação banda base:")
        baseband_label.pack(pady=5)
        baseband_frame = ttk.Frame(self.protocol_window)
        baseband_frame.pack(pady=5)
        ttk.Radiobutton(baseband_frame, text="NRZ Polar", variable=self.protocol_vars['baseband'], 
                       value="polar_nrz").pack()
        ttk.Radiobutton(baseband_frame, text="NRZ Bipolar", variable=self.protocol_vars['baseband'], 
                       value="bipolar_nrz").pack()
        ttk.Radiobutton(baseband_frame, text="Manchester", variable=self.protocol_vars['baseband'], 
                       value="manchester").pack()

        # Carrier Modulation
        carrier_label = tk.Label(self.protocol_window, text="Escolha o protocolo de modulação de portadora:")
        carrier_label.pack(pady=5)
        carrier_frame = ttk.Frame(self.protocol_window)
        carrier_frame.pack(pady=5)
        ttk.Radiobutton(carrier_frame, text="ASK", variable=self.protocol_vars['carrier'], 
                       value="ask", command=lambda: self.show_carrier_params("ask")).pack()
        ttk.Radiobutton(carrier_frame, text="FSK", variable=self.protocol_vars['carrier'], 
                       value="fsk", command=lambda: self.show_carrier_params("fsk")).pack()
        ttk.Radiobutton(carrier_frame, text="QAM-8", variable=self.protocol_vars['carrier'], 
                       value="qam8", command=lambda: self.show_carrier_params("qam8")).pack()

        # Parameters Frame
        self.params_frame = ttk.Frame(self.protocol_window)
        self.params_frame.pack(pady=10)

        # Show initial carrier params
        self.show_carrier_params("ask")

        # Submit Button
        submit_button = ttk.Button(self.protocol_window, text="Confirmar", 
                                 command=self.protocol_window.destroy)
        submit_button.pack(pady=10)

    def show_carrier_params(self, carrier_type):
        # Clear previous parameters
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        # Common parameter
        tk.Label(self.params_frame, text="Amplitude:").pack()
        ttk.Entry(self.params_frame, textvariable=self.protocol_vars['amplitude']).pack()

        if carrier_type == "ask" or carrier_type == "qam8":
            tk.Label(self.params_frame, text="Frequência:").pack()
            ttk.Entry(self.params_frame, textvariable=self.protocol_vars['frequency']).pack()
        elif carrier_type == "fsk":
            tk.Label(self.params_frame, text="Frequência para '0':").pack()
            ttk.Entry(self.params_frame, textvariable=self.protocol_vars['freq0']).pack()
            tk.Label(self.params_frame, text="Frequência para '1':").pack()
            ttk.Entry(self.params_frame, textvariable=self.protocol_vars['freq1']).pack()

    def process_message(self, message: str):
        data = [ord(char) for char in message]

        # Create protocol window and wait for user input
        self.create_protocol_window()
        self.protocol_window.wait_window()

        # Get selected protocols
        framing_protocol = self.protocol_vars['framing'].get()
        error_detection_protocol = self.protocol_vars['error_detection'].get()
        baseband_protocol = self.protocol_vars['baseband'].get()
        carrier_protocol = self.protocol_vars['carrier'].get()

        # Apply framing
        framed_message = byte_insertion(data) if framing_protocol == "byte_insertion" else char_count(data)

        # Apply error detection
        error_checked_message = (compute_parity_bit(framed_message) 
                               if error_detection_protocol == "parity_bit" 
                               else append_crc32(framed_message))

        bits = bytes_to_bits(error_checked_message)
        encoded_message = encode_hamming(bits)

        # Apply baseband modulation
        if baseband_protocol == "polar_nrz":
            modulated_message = polar_nrz(encoded_message)
        elif baseband_protocol == "bipolar_nrz":
            modulated_message = bipolar_nrz(encoded_message)
        else:
            modulated_message = manchester(encoded_message)

        # Apply carrier modulation
        try:
            amplitude = float(self.protocol_vars['amplitude'].get() or "1.0")
            if carrier_protocol == "ask":
                frequency = float(self.protocol_vars['frequency'].get() or "1000.0")
                modulated_message = ask_modulation(modulated_message, amplitude, frequency)
                freq0 = freq1 = 0
            elif carrier_protocol == "fsk":
                freq0 = float(self.protocol_vars['freq0'].get() or "1000.0")
                freq1 = float(self.protocol_vars['freq1'].get() or "2000.0")
                modulated_message = fsk_modulation(modulated_message, amplitude, freq0, freq1)
            else:  # qam8
                frequency = float(self.protocol_vars['frequency'].get() or "1000.0")
                modulated_message = qam8_modulation(modulated_message, amplitude, frequency)
                freq0 = freq1 = 0
        except ValueError:
            self.update_info_label("Erro: Por favor, insira valores numéricos válidos para os parâmetros.")
            return None, None

        protocol_config = {
            "framing": framing_protocol,
            "error_detection": error_detection_protocol,
            "baseband": baseband_protocol,
            "carrier": carrier_protocol,
            "threshold": 0.5,
            "amplitude": amplitude,
            "f0": freq0,
            "f1": freq1,
        }

        return encoded_message, protocol_config

    def update_info_label(self, text):
        if self.info_label:
            self.info_label.config(text=text)

    def handle_message(self, message: str):
        if message.lower() == "sair":
            self.update_info_label("[INFO] Encerrando cliente.")
            self.client.close()
            self.gui.close()
            return

        try:
            # Divide a mensagem
            parts = self.fragment_message(message, 4)
            num_parts = len(parts)
            # Envia o número de partes
            self.client.sendall(str(num_parts).encode())

            # Para cada parte da mensagem
            for part in parts:
                # Processa a parte com os protocolos
                result = self.process_message(part)
                if result is None:
                    continue
                processed_message, protocol_config = result
                
                # Envia mensagem ao servidor
                self.client.sendall(str((processed_message, protocol_config)).encode())
                # Recebe resposta do servidor
                response = self.client.recv(1024).decode()
                self.update_info_label(f"Resposta sobre a parte: {response}")

            # Recebe resposta do servidor
            response = self.client.recv(1024).decode()
            self.update_info_label(f"Resposta do servidor: {response}")

        except Exception as e:
            self.update_info_label(f"[ERROR] {e}")

    def start(self):
        try:
            self.client.connect((self.host, self.port))
            
            # Create main GUI
            self.gui = ClientGUI(message_callback=self.handle_message)
            
            # Add info label to GUI
            self.info_label = tk.Label(self.gui.root, text=f"[INFO] Conectado a {self.host}:{self.port}", 
                                     wraplength=300)
            self.info_label.pack(pady=10)
            
            # Start GUI
            self.gui.start()

        except Exception as e:
            if self.gui and self.info_label:
                self.update_info_label(f"[ERROR] {e}")
            else:
                print(f"[ERROR] {e}")
        finally:
            self.client.close()
            if self.gui and self.info_label:
                self.update_info_label("[INFO] Cliente encerrado.")

if __name__ == "__main__":
    client = ProtocolClient()
    client.start()