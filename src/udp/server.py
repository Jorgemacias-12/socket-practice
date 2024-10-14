import threading
import socket
import sys
import os

from colorama import init, Fore, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import get_machine_ip, list_folder_contents, convert_to_table

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
                try:
                    files = list_folder_contents()

                    if not files:
                        server.sendto(f"{Fore.YELLOW}No hay ningún archivo que mostrar{Style.RESET_ALL}".encode(), address)
                        print(f"{Fore.LIGHTMAGENTA_EX}Respuesta enviada a {address}{Style.RESET_ALL}")
                    
                    response = convert_to_table(files)
                                
                    server.sendto(f"\n{Fore.LIGHTBLUE_EX}{response}{Style.RESET_ALL}".encode(), address)
                    print(f"{Fore.LIGHTMAGENTA_EX}Respuesta enviada a {address}{Style.RESET_ALL}")
                    server.sendto(f"\n{Fore.YELLOW}Si deseas descargar algún archivo, utiliza el comando get, y el índice del archivo que deseas descargar.{Style.RESET_ALL}\n".encode(), address)
                except Exception as e:
                    print(e)
                    
            if "get" in decoded_message:
                print("Enviar archivo al cliente")
                    
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
