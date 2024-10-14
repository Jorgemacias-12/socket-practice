from utils.index import list_folder_contents
from utils.index import get_machine_ip
from utils.index import generate_random_port
import threading
import socket
import sys
import os

from colorama import init, Fore, Style, Back

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


server_config = (
    get_machine_ip(),
    20000
)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(server_config)

init(convert=True)

print(f"{Fore.GREEN}Servidor iniciado en {server_config[0]}:{
      server_config[1]}, esperando conexiones..")

connections = []
stop_server = False
available_commands = ["list", "get"]


def accept_connections():
    global stop_server
    global available_commands
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
                    response = "test".encode()

                    server.sendto(response, address)
                except Exception as e:
                    print(e)

            # for command in available_commands:
            #   if command == "list" and command in decoded_message:
            #     try:
            #       files = list_folder_contents()

            #       print(files)

            #       if not files:
            #         server.sendto("Hola mundo".encode(), address)
            #     except Exception as e:
            #       print(e)

        except KeyboardInterrupt:
            stop_server = True
            server.close()
            print(f"{Fore.RED}\nCerrando servidor...{Style.RESET_ALL}")
        except Exception as e:
            stop_server = True
            server.close()
            print(f"{Fore.RED}\nCerrando servidor con código de error {
                  e}{Style.RESET_ALL}")


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
