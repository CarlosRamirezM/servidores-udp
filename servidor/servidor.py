# Script del servidor TCP

from fileinput import filename
from pickletools import read_bytes1
import hashlib
import stopwatch as sw
import socket
from stat import filemode
import threading
from tkinter import SEPARATOR
import logging
from datetime import datetime
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(25)

def process_thread(filename, client_socket, barrier, hash):
    try:
        while True:
            num_client = client_socket.recv(1024).decode('utf-8')
            print('Num client',num_client)
            request = client_socket.recv(1024)
            if not request or request.decode('utf-8') == 'END':
                break

            str_req = request.decode("utf-8").split(' ')
            print(f"received {str_req} from client")
            if str_req[0] == 'LISTO':
                barrier.wait()   
    
            print('mandando archivo',filename)
            ti = sw.start()
            with open(filename,"rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    client_socket.sendall(bytes_read)
            client_socket.send('DONE'.encode('utf-8'))

            request = client_socket.recv(1024)
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
    num_clients , file = [int(x) for x in input("Ingrese el numero de clientes y el archivo (ej: 5 100)").split()]
    selectedFile = f'servidor/files/{file}.bin'
    barrier = threading.Barrier(num_clients)

    now = datetime.now()  # current date and time
    now_str = now.strftime("%Y-%m-%d-%I-%M-%S")

    logging.basicConfig(filename=f'./Logs/{now_str}-log.txt', filemode='w',
                    encoding='utf-8', datefmt='', level=logging.INFO)
    logging.info("LOG INICIADO SERVER")

    with open(selectedFile,"rb") as f:
        bytes = f.read() # read entire file as bytes
        hash = hashlib.sha256(bytes).digest()
        print(hash)

    for i in range(num_clients):
        print("Esperando conexiones")
        client_socket, addr = server_socket.accept()    
        print("client connected from", addr)
        cliente = threading.Thread(target=process_thread, args=(selectedFile,client_socket,barrier,hash,))
        cliente.start()
       

   
