# Script del servidor TCP

import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(2)

while True:
    print("Esperando conexiones")
    client_socket, addr = server_socket.accept()
    print("client connected from", addr)
    while True:
        data = client_socket.recv(1024)
        if not data or data.decode('utf-8') == 'END':
            break
        str_data = data.decode("utf-8")
        print(f"received {str_data} from client")
        try:
            client_socket.send(bytes('Hey', 'utf-8'))
        except:
            print("Exited by user")
            server_socket.close()
    client_socket.close()
