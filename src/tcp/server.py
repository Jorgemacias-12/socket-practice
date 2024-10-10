import threading 
import datetime
import socket
import sys
import os

from colorama import init, Fore, Back, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import generate_random_port

server_config = (
  socket.gethostname(),
  generate_random_port()
)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(server_config)
server.listen(1)

init()

print(f"{Fore.GREEN}Servidor iniciado en {server_config[0]}:{server_config[1]}, esperando conexiones..")

clients = []
stop_server = False

def handle_connections(connection, address):
  print(f"{Back.YELLOW}{Fore.WHITE} Se ha conectado -> {address} {Style.RESET_ALL}")
  
  clients.append((connection, address))
  
  try:
    while True:
      data = connection.recv(1024)
      isCommand = None
      
      if "get date" in data.decode():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        connection.sendall(now.encode())
        isCommand = True

      if "get participants" in data.decode():
        connected_users = ', '.join(f"({conn.fileno()}, {addr})" for conn, addr in clients)
        connection.sendall(connected_users.encode())
        isCommand = True
          
      if not data:
        break
      
      print(f"{Fore.WHITE} {data.decode()}")
      
      for client, addr in clients:
        if data.decode() == "get date": break
        if data.decode() == "get participants": break
        if addr != address and not isCommand:
          client.sendall(data)
  except ConnectionResetError:
    pass
  finally:
    connection.close()
    clients.remove((connection, address))

def accept_connections():
  global stop_server
  
  while not stop_server:
    try:
      connection, address = server.accept()
      
      thread = threading.Thread(target=handle_connections, args=(connection, address))
      thread.start()
    except OSError:
      break
    
def main():
  global stop_server
  try:
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

    while True:
      pass

  except KeyboardInterrupt:
    stop_server = True
    
    print(f"{Fore.RED}\nCerrando servidor...{Style.RESET_ALL}")
    
    for client, _ in clients:
      client.close()
    
    server.close()
    accept_thread.join()

if __name__ == "__main__":
  main()