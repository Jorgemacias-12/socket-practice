import socket
import random
import threading
from colorama import init, Back, Fore, Style

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("192.168.100.7", 4000)

client.connect(server_address)

username = f"User-{random.randint(0, 4000)}"

init()

client.send(f"{username} se ha conectado".encode())

def handle_message_from_server():
  while True:
    try:
      data = client.recv(1024)
    
      if data:
        print(f"\n {Fore.YELLOW} {data.decode()} \n {Style.RESET_ALL}")
    except:
      break
    
thread = threading.Thread(target=handle_message_from_server)
thread.start()

while True:
  message = input("> ")
  
  if message.strip() == "": continue
  
  if "exit" in message:
    client.send(f"{username} se ha desconectado".encode())
    break    
  
  final_message = username + " " + message
  client.send(final_message.encode())

client.close();