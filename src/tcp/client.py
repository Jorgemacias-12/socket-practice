import threading
import socket
import sys
import os

from colorama import init, Fore, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import validate_ip, validate_port

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(5.0) # Five seconds :P

init()

username = None

def handle_message_from_server():
    while True:
        try:
            data = client.recv(1024)
            
            if data:
                print(f"{Fore.CYAN}{Style.RESET_ALL}{Fore.MAGENTA}{data.decode()}{Style.RESET_ALL}\n")
                
        except socket.timeout:
            print(f"{Fore.RED}No se recibió respuesta del servidor en el tiempo esperado{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            client.close()
            break

def handle_message_send():
    while True:
        message = input(f"{Fore.CYAN}> {Style.RESET_ALL}")
        
        if message.strip() == "":
            continue
        
        if "exit" in message:
            client.send(f"{username} se ha desconectado".encode())
            break
        
        message = f"{Fore.YELLOW}[{username}] {Style.RESET_ALL}{message}"
        
        client.send(message.encode())

def main():
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
        global username
        
        username = input(f"{Fore.CYAN}Ingrese su nombre de usuario: {Style.RESET_ALL}")

        if username != "":
            break
        else:
            print(f"{Fore.RED}Por favor, eliga un nombre de usuario para continuar. {
                  Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}Conectando a {server_addr} en el puerto {server_port}...{Style.RESET_ALL}")
    
    try:
        client.connect((server_addr, server_port))
        
        print(f"{Fore.GREEN}Te has conectado! {Style.RESET_ALL}")
        
        client.send(f"{Fore.YELLOW}[{username}]{Style.RESET_ALL} se ha conectado".encode())
        
        recieve_thread = threading.Thread(target=handle_message_from_server)
        send_thread = threading.Thread(target=handle_message_send)

        recieve_thread.start()
        send_thread.start()
        
        while True:
            pass        
    except Exception as e:
        print(f"{Fore.RED}No se ha podido conectar al servidor: {e}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Desconectando...{Style.RESET_ALL}")
    finally:
        client.send(f"{username} se ha desconectado".encode())
        client.close()
    
if __name__ == "__main__":
    main()