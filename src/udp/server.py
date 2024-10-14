import threading
import socket
import sys
import os
import re

from colorama import init, Fore, Style

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.index import get_file_full_path, get_machine_ip, list_folder_contents, convert_to_table

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
available_files = []

def accept_connections():
    global stop_server
    global server
    global available_files

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
                    available_files = list_folder_contents()

                    if not available_files:
                        server.sendto(f"{Fore.YELLOW}No hay ningún archivo que mostrar{Style.RESET_ALL}".encode(), address)
                        print(f"{Fore.LIGHTMAGENTA_EX}Respuesta enviada a {address}{Style.RESET_ALL}")
                    
                    response = convert_to_table(available_files)
                                
                    server.sendto(f"\n{Fore.LIGHTBLUE_EX}{response}{Style.RESET_ALL}".encode(), address)
                    print(f"{Fore.LIGHTMAGENTA_EX}Respuesta enviada a {address}{Style.RESET_ALL}")
                    server.sendto(f"\n{Fore.YELLOW}Si deseas descargar algún archivo, utiliza el comando get, y el índice del archivo que deseas descargar.{Style.RESET_ALL}\n".encode(), address)
                except Exception as e:
                    print(e)
                    
            if "get" in decoded_message:
                if not available_files:
                    available_files = list_folder_contents()
                
                match = re.search(r'get\s+(\d+)', decoded_message)
                
                if match:
                    file_index = int(match.group(1))
                    
                    if 0 <= file_index < len(available_files):
                        file_name = available_files[file_index][0]
                        file_path = get_file_full_path(file_name)
                        
                        server.sendto(b'Sending file', address)
                        server.sendto(f'filename [{file_name}]'.encode(), address)
                        
                        confirmation, _ = server.recvfrom(1024)
                        confirmation = confirmation.decode()
                        
                        if "ready" in confirmation:
                            try:
                                with open(file_path, 'rb') as file:
                                    data = file.read(1024)
                                    
                                    while data:
                                        server.sendto(data, address)
                                        data = file.read(1024)
                                server.sendto(b'finish', address)
                            except Exception as e:
                                server.sendto(f"\n{Fore.RED}Error al enviar el archivo: {e}{Style.RESET_ALL}\n".encode(), address)
                    else:
                        server.sendto(f"\n{Fore.RED}Índice no válido, utiliza list para ver los archivos disponibles, o intentalo de nuevo.{Style.RESET_ALL}\n".encode(), address)   
                else:
                    server.sendto(f"\n{Fore.RED}Índice no válido, utiliza list para ver los archivos disponibles, o intentalo de nuevo.{Style.RESET_ALL}\n".encode(), address)
        
                    
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
