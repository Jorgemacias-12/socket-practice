import threading
import datetime
import socket
import sys
import os 
import colorama

from colorama import init, Fore, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import generate_random_port
from utils.index import get_machine_ip

server_config = (
  get_machine_ip(),
  generate_random_port()
)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(server_config)
server.listen(1)

init(convert=True)

print(f"{Fore.GREEN}Servidor iniciado en {server_config[0]}:{server_config[1]}, esperando conexiones..")

clients = []
stop_server = False