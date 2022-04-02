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

#ip = '192.168.146.128'
ip = '127.0.0.1'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, 21))
PAYLOAD = 64*(2**10)


def process_thread(filename, address, numClient):
    try:
                 
        print('Num. cliente', numClient)
        request = server_socket.recvfrom(PAYLOAD)
        print("Request",request)
        str_req = request.decode("utf-8").split(' ')
        print(f"Recibido {str_req} del cliente")

        if str_req[0] == 'LISTO':
            print('Enviando archivo', filename)
            ti = sw.start()
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(PAYLOAD)
                    if not bytes_read:
                        print('Último chunk')
                        break
                    server_socket.sendto(bytes_read, address)
                    sleep(2)
                    server_socket.sendto('DONE'.encode('utf-8'), address)
                    print("Se mandó el DONE")
            
            tf = sw.end()                              
            tamanio = os.path.getsize(filename)
            logging.info(f"Entrega exitosa \
                            \n Se envió el archivo: {filename} de tamaño: {tamanio} bytes \
                            \n Enviado al cliente {numClient} \
                            \n {sw.dar_duracion(ti,tf)}")
    except:
        logging.info(f"Entrega no exitosa \
                        \n Cliente {numClient}")


while True:   
    num_clients, file = [int(x) for x in input().split()]
    selectedFile = f'servidor/files/{file}.bin'

    now = datetime.now()  # current date and time
    now_str = now.strftime("%Y-%m-%d-%I-%M-%S")

    logging.basicConfig(filename=f'./Logs/{now_str}-log.txt', filemode='w',
                        encoding='utf-8', datefmt='', level=logging.INFO)
    logging.info("LOG INICIADO SERVER")    

    for i in range(num_clients):
        print("Esperando conexiones")
        numClient, addr = server_socket.receiveFrom(PAYLOAD)
        print("client connected from", addr)
        cliente = threading.Thread(target=process_thread, args=(selectedFile, addr, numClient))
        cliente.start()
