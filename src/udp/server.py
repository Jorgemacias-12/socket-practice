import threading
import socket
import sys
import os

from colorama import init, Fore, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import get_machine_ip, list_folder_contents

server_config = (
    get_machine_ip(),
    20000
)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_config)

init(convert=True)

print(f"{Fore.GREEN}Servidor iniciado en {server_config[0]}:{server_config[1]}, esperando conexiones..{Style.RESET_ALL}")

connections = []
stop_server = False
available_commands = ["list", "get"]

def accept_connections():
    global stop_server
    global server

    while not stop_server:
        try:
            message, address = server.recvfrom(1024)

            if address not in connections:
                connections.append(address)

            print(f"{Fore.MAGENTA}Mensaje desde {address} {Style.RESET_ALL}")
            print(f"{message.decode()}")

            decoded_message = message.decode()

            if "list" in decoded_message:
                print("Si")
                try:
                    files = list_folder_contents()

                    if not files:
                        server.sendto(f"{Fore.YELLOW}No hay ningún archivo que mostrar".encode(), address)
                        print(f"{Fore.LIGHTMAGENTA_EX}Respuesta enviaa a {address}{Style.RESET_ALL}")
                        
                    server.sendto(str(files).encode(), address)
                    print(f"{Fore.LIGHTMAGENTA_EX}Respuesta enviaa a {address}{Style.RESET_ALL}")
                except Exception as e:
                    print(e)
                    
        except OSError as e:
            if not stop_server:
                print(f"{Fore.RED}\nError de socket: {e}{Style.RESET_ALL}")
            break
        except Exception as e:
            if not stop_server:
                print(f"{Fore.RED}\nError inesperado: {e}{Style.RESET_ALL}")
            break

def main():
    global stop_server

    try:
        connections_thread = threading.Thread(target=accept_connections)
        connections_thread.start()

        while True:
            pass
    except KeyboardInterrupt:
        stop_server = True
        print(f"{Fore.RED}\nCerrando servidor...{Style.RESET_ALL}")
        server.close()
        connections_thread.join()

if __name__ == "__main__":
    main()
