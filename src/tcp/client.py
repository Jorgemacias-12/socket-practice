import threading 
import socket
import sys
import os

from colorama import init, Fore, Back, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import validate_ip, validate_port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

init()

username = None

def handle_message_from_server():
  while True:
    try:
      data = client.recv(1024)
      
      if data:
        print(f"\n {Fore.YELLOW}{data.decode()} \n {Style.RESET_ALL}")
    except:
      pass

def handle_message_send():
  while True:
    message = input(f"{Fore.CYAN}> {Style.RESET_ALL}")
  
    if message.strip() == "": continue

    if "exit" in message:
      client.send(f"{username} se ha desconectado".encode())
      break
    
    message = f"{Fore.YELLOW}[{username}] {Style.RESET_ALL} {message}"
    
    client.send(message.encode())

def main():
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
    global username    
    username = input(f"Ingrese su nombre de usuario: ")
    
    if username != "":
      break
    else:
      print(f"{Fore.RED}Por favor, eliga un nombre de usuario para continuar. {Style.RESET_ALL}")
  
  print(f"{Fore.GREEN}Conectando a {server_addr} en el puerto {server_port}...{Style.RESET_ALL}")
  
  try:
    client.connect((server_addr, server_port))
    
    print(f"{Fore.GREEN}Conexión exitosa! {Style.RESET_ALL}")
    
    client.send(f"{username} Se ha connectado".encode())
    
    recieve_thread = threading.Thread(target=handle_message_from_server)
    send_thread = threading.Thread(target=handle_message_send)
    
    recieve_thread.start()
    send_thread.start()
    
    recieve_thread.join()
    send_thread.join()
  except Exception as e:
    print(f"{Fore.RED}No se ha podido conectar al servidor: {e}{Style.RESET_ALL}")
  print(f"\n{Fore.RED}Desconectando...{Style.RESET_ALL}")
  
  client.send(f"{username} se ha desconectado".encode())
  client.close()
  
  sys.exit(0)
  print(f"{Fore.RED}No se ha podido conectar al servidor: {e}{Style.RESET_ALL}")    
  
    
if __name__ == "__main__":
  main()