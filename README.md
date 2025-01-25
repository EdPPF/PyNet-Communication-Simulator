## Como rodar o projeto

Clone o repositório:

```bash
git clone https://github.com/EdPPF/PyNet-Communication-Simulator.git
cd PyNet-Communication-Simulator
```

TODO

## Estrutura do Repositório

```bash
IP_sim/
├── client/                      # Código relacionado ao Cliente
│   ├── client.py                # Implementação principal do Cliente
│   └── gui/                     # Interface gráfica do Cliente
│       └── gui.py               # Implementação da GUI do Cliente
├── server/                      # Código relacionado ao Servidor
│   ├── server.py                # Implementação principal do Servidor
│   └── gui/                     # Interface gráfica do Servidor
│       └── gui.py               # Implementação da GUI do Servidor
├── link_layer/                  # Implementação da Camada de Enlace
│   ├── framing/                 # Protocolos de enquadramento
│   │   ├── char_count.py        # Contagem de caracteres
│   │   └── byte_insertion.py    # Inserção de bytes ou caracteres
│   ├── error_detection/         # Detecção de erros
│   │   ├── parity_bit.py        # Bit de paridade
│   │   └── crc.py               # CRC-32
│   └── error_correction/        # Correção de erros
│       └── hamming.py           # Código de Hamming
├── physical_layer/              # Implementação da Camada Física
│   ├── baseband_modulation/     # Modulações banda-base
│   │   ├── nrz_polar.py         # Modulação NRZ-Polar
│   │   ├── manchester.py        # Modulação Manchester
│   │   └── bipolar.py           # Modulação Bipolar
│   ├── carrier_modulation/      # Modulações por portadora
│   │   ├── ask.py               # Modulação ASK
│   │   ├── fsk.py               # Modulação FSK
│   │   └── qam_8.py             # Modulação 8-QAM
├── common/                      # Código compartilhado entre cliente e servidor
│   ├── utils/                   # Utilidades gerais
│   │   ├── encoding.py          # Funções auxiliares de codificação
│   │   └── math.py              # Funções matemáticas úteis
│   ├── communication/           # Sockets
│   │   ├── socket_client.py
│   │   ├── socket_server.py
│   │   └── protocol.py          # Protocolo de comunicação
│   └── constants.py             # Constantes compartilhadas
├── main.py                      # Ponto de entrada da aplicação
├── go.mod                       # Gerenciamento de dependências do Go
├── .gitignore
└── README.md
```
