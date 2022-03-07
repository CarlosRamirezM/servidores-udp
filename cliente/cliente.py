# Script para el cliente

import socket


def crear_conexion(numero_cliente: int):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Cambiar al puerto 20 en produccion
        client_socket.connect(('127.0.0.1', 12345))
        print("Conexión exitosa")
    except:
        print("Conexión no exitosa. Vuelva a intentarlo.")
    payload = 'Hey Server'

    try:
        while True:
            client_socket.send(payload.encode('utf-8'))
            data = client_socket.recv(1024)
            more = input("¿Cuál archivo quiere escoger?")

    except KeyboardInterrupt:
        print("Exited by user")
    client_socket.close()
