# Script del servidor TCP

from fileinput import filename
from pickletools import read_bytes1
import hashlib
import stopwatch as sw
import socket
from stat import filemode
import threading
import logging
from datetime import datetime
import os
from time import sleep

ip = '192.168.146.128'
#ip = '127.0.0.1'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, 21))
server_socket.listen(25)
TAMANIO_CHUNK = 4096


def process_thread(filename, client_socket, barrier, hash):
    try:
        while True:
            num_client = client_socket.recv(TAMANIO_CHUNK).decode('utf-8')
            print('Num. cliente', num_client)
            request = client_socket.recv(TAMANIO_CHUNK)
            if not request or request.decode('utf-8') == 'END':
                break

            str_req = request.decode("utf-8").split(' ')
            print(f"Recibido {str_req} del cliente")
            if str_req[0] == 'LISTO':
                barrier.wait()

            print('Enviando archivo', filename)
            ti = sw.start()
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(TAMANIO_CHUNK)
                    if not bytes_read:
                        print('Último chunk')
                        break
                    client_socket.sendall(bytes_read)
            sleep(1)
            client_socket.send('DONE'.encode('utf-8'))
            print("Se mandó el DONE")

            request = client_socket.recv(TAMANIO_CHUNK)
            tf = 0
            if request.decode('utf-8') == 'ULTIMO_PAQUETE':
                tf = sw.end()
                client_socket.sendall(hash)
            tamanio = os.path.getsize(filename)
            logging.info(f"Entrega exitosa \
                        \n Se envió el archivo: {filename} de tamaño: {tamanio} bytes \
                        \n Enviado al cliente {num_client} \
                        \n {sw.dar_duracion(ti,tf)}")
    except:
        logging.info(f"Entrega no exitosa \
                        \n Cliente {num_client}")


while True:
    readyCount = 0
    num_clients, file = [int(x) for x in input().split()]
    selectedFile = f'servidor/files/{file}.bin'
    barrier = threading.Barrier(num_clients)

    now = datetime.now()  # current date and time
    now_str = now.strftime("%Y-%m-%d-%I-%M-%S")

    logging.basicConfig(filename=f'./Logs/{now_str}-log.txt', filemode='w',
                        encoding='utf-8', datefmt='', level=logging.INFO)
    logging.info("LOG INICIADO SERVER")

    with open(selectedFile, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        hash = hashlib.sha256(bytes).digest()

    for i in range(num_clients):
        print("Esperando conexiones")
        client_socket, addr = server_socket.accept()
        print("client connected from", addr)
        cliente = threading.Thread(target=process_thread, args=(
            selectedFile, client_socket, barrier, hash,))
        cliente.start()
