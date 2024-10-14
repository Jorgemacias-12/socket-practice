import threading
import socket
import sys
import os

from colorama import init, Fore, Style, Back

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import validate_ip
from utils.index import validate_port

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = None
server_addr = None
server_port = None
lock = threading.Lock()
socket_open = True

init()

def close_socket():
  global socket_open
  with lock:
    if socket_open:
      socket_open = False
      client.close()

def handle_messages():
  global client, socket_open
  
  try:
    while True:
      message = input(f"{Fore.CYAN}> {Style.RESET_ALL}")
      
      if message == "":
        continue
      
      message = f"{Fore.YELLOW}[{username}] {Style.RESET_ALL}{message}".encode()
      
      with lock:
        if socket_open:
          client.sendto(message, (server_addr, server_port))
  except Exception as e:
    print(f"\n{Fore.RED}Error al recibir el mensaje: {e}{Style.RESET_ALL}")
    close_socket()
    
def handle_recieve_messages():
  global client, socket_open
  
  try:
    while True:
      data, addr = client.recvfrom(4096)
      
      if data:
        print(data.decode())
  except Exception as e:
    print(f"\n{Fore.RED}Error al recibir respuesta desde el servidor, error detallado: {e}{Style.RESET_ALL}")
    
def main():
  global server_addr, server_port, username
  
  while True:
    server_addr = input(f"{Fore.CYAN}Ingrese la dirección del servidor: {Style.RESET_ALL}")
    
    if server_addr == "localhost":
      server_addr = "127.0.0.1"
    
    if validate_ip(server_addr):
      break
    else:
      print(f"{Fore.RED}Dirección IP no válida. Intente de nuevo.{Style.RESET_ALL}") 
  
  while True:
    server_port = input(f"{Fore.CYAN}Ingrese el puerto del servidor: {Style.RESET_ALL}")
    
    if validate_port(server_port):
      server_port = int(server_port)
      break
    else:
      print(f"{Fore.RED}Puerto no válido. Debe ser un número entre 1 y 65535.{Style.RESET_ALL}")
  
  while True:
    username = input(f"{Fore.CYAN}Ingrese su nombre de usuario: {Style.RESET_ALL}")
    
    if username != "":
      break
    else:
      print(f"{Fore.RED}Por favor, eliga un nombre de usuario para continuar. {Style.RESET_ALL}")
  
  messages_thread = threading.Thread(target=handle_messages)
  recieve_thread = threading.Thread(target=handle_recieve_messages)
  
  messages_thread.start()
  recieve_thread.start()  
  
if __name__ == "__main__":
  main()