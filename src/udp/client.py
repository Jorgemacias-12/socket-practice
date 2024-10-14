import threading
import socket
import sys
import os 

from colorama import init, Fore, Style, Back

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import validate_ip
from utils.index import validate_port

init(convert=True)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
username = None
server_addr = None
server_port = None

def handle_messages():
  try:
    while True:
      message = input(f"{Fore.CYAN}> {Style.RESET_ALL}")
      
      if message == "":
        continue
      
      message = f"{Fore.YELLOW}[{username}] {Style.RESET_ALL}{message}" 
      
      client.sendto(message.encode(), (server_addr, server_port))
  except KeyboardInterrupt:
    print(f"\n{Fore.RED}Saliendo... {Style.RESET_ALL}")
    
    client.sendto(f'{username} se ha desconectado del servidor'.encode(), (server_addr, server_port))
    client.close()
    
    sys.exit()

def handle_recieve_messages():
  try:
    while True:
      data, address = client.recvfrom(1024)
      
      if data:
        print(data.decode())   

  except Exception as e: 
    print(e)

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
  
  messages_thread.join()
  recieve_thread.join()
      
if __name__ == "__main__":
  main()