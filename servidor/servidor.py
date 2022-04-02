# Script del servidor UDP
import stopwatch as sw
import socket
import threading
import logging
from datetime import datetime
import os
from time import sleep

ip = '192.168.65.128'
#ip = '127.0.0.1'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, 12345))
PAYLOAD = 50000


def process_thread(filename, address, numClient):
    try:

        print('Num. cliente', int(numClient)-1)
        request = server_socket.recvfrom(PAYLOAD)
        str_req = request[0].decode("utf-8")
        print(f"Recibido {str_req} del cliente")

        if str_req == 'LISTO':
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
                            \n Enviado al cliente {int(numClient)-1} \
                            \n {sw.dar_duracion(ti,tf)}")
    except Exception as e:
        print(e)
        logging.info(f"Entrega no exitosa \
                        \n Cliente {int(numClient)-1}")


while True:
    num_clients, file = [int(x) for x in input().split()]
    selectedFile = f'./files/{file}.bin'

    now = datetime.now()  # current date and time
    now_str = now.strftime("%Y-%m-%d-%I-%M-%S")

    logging.basicConfig(filename=f'./Logs/{now_str}-log.txt', filemode='w',
                        encoding='utf-8', datefmt='', level=logging.INFO)
    logging.info("LOG INICIADO SERVER")

    for i in range(num_clients):
        print("Esperando conexiones")
        numClient, addr = server_socket.recvfrom(PAYLOAD)
        print("client connected from", addr)
        cliente = threading.Thread(
            target=process_thread, args=(selectedFile, addr, numClient.decode("utf-8"),))
        cliente.start()
