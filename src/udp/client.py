import socket
import sys
import os
import threading

from colorama import init, Fore, Style


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import validate_port
from utils.index import validate_ip

TIMEOUT = 5

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(TIMEOUT)

init()

def recieve_messages():
    while True:
        try:
            data, server = client.recvfrom(1024)
                        
            print(f"{data.decode()}")
        except socket.timeout:
            pass 
        except Exception as e:
            print(f"\n{Fore.RED}{e}{Style.RESET_ALL}")

def main():
    global server_addr, server_port, username

    while True:
        server_addr = input(
            f"{Fore.CYAN}Ingrese la dirección del servidor: {Style.RESET_ALL}")

        if server_addr == "localhost":
            server_addr = "127.0.0.1"

        if validate_ip(server_addr):
            break
        else:
            print(f"{Fore.RED}Dirección IP no válida. Intente de nuevo.{
                Style.RESET_ALL}")

    while True:
        server_port = input(
            f"{Fore.CYAN}Ingrese el puerto del servidor: {Style.RESET_ALL}")

        if validate_port(server_port):
            server_port = int(server_port)
            break
        else:
            print(f"{Fore.RED}Puerto no válido. Debe ser un número entre 1 y 65535.{
                Style.RESET_ALL}")

    while True:
        username = input(f"{Fore.CYAN}Ingrese su nombre de usuario: {
                        Style.RESET_ALL}")

        if username != "":
            break
        else:
            print(f"{Fore.RED}Por favor, eliga un nombre de usuario para continuar. {
                Style.RESET_ALL}")
    
    recieve_thread = threading.Thread(target=recieve_messages)
    recieve_thread.daemon = True
    recieve_thread.start()
    
    try:
        while True:
            message = input(f"{Fore.CYAN}> {Style.RESET_ALL}")

            if message == "":
                continue
            if "exit" in message:
                print(f"{Fore.RED}Finalizando sesión como {username}, cerrando cliente...{Style.RESET_ALL}")
                break
            
            message = f"{Fore.YELLOW}[{username}] {Style.RESET_ALL}{message}"
            
            client.sendto(message.encode(), (server_addr, server_port))
    except KeyboardInterrupt:
        print(f"{Fore.RED}Finalizando sesión como {username}, cerrando cliente...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()