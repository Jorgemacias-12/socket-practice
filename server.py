import socket
import threading
import datetime
from colorama import init, Fore, Back, Style

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("192.168.100.7", 4000))
server.listen(1)

init()

print(f"{Fore.GREEN} Servidor iniciado, esperando conexiones")

clients = []

def handle_connections(connection, address):
  
  print(f"{Back.YELLOW} {Fore.WHITE} Se ha connectado -> {address} {Style.RESET_ALL}")
  
  clients.append((connection, address))
  
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
      if addr != address and not isCommand:
        client.sendall(data)
  
  connection.close()
  clients.remove((connection, address))

while True:
  connection, address = server.accept()
  
  thread = threading.Thread(target=handle_connections, args=(connection, address))
  thread.start()