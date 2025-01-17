import socket
import logging
import os
import stopwatch as sw
from time import sleep

LISTO = 'LISTO'
PAYLOAD = 50000

ip = '192.168.146.128'
#ip = '127.0.0.1'

server_address_port = (ip, 12345)


def crear_conexion(numero_cliente: int, cantidad_conexiones: int):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client_socket.sendto(f'{numero_cliente+1}'.encode(
            'utf-8'), server_address_port)
        print(f"Conexión exitosa cliente {numero_cliente}")
        logging.info(f"Conexión hecha para cliente {numero_cliente}")
    except:
        print("Conexión no exitosa. Vuelva a intentarlo.")
    try:
        while True:

            listo = 's'

            if listo == 's':

                nombre_archivo = f"./ArchivosRecibidos/Cliente{numero_cliente}-Prueba{cantidad_conexiones}.txt"
                client_socket.sendto(LISTO.encode(
                    'utf-8'), server_address_port)
                archivo = open(nombre_archivo, "wb+")

                primero = True
                paquete = client_socket.recvfrom(PAYLOAD)[0]
                while True:

                    try:
                        if paquete.decode('utf-8') == 'DONE':
                            print("Se recibe un DONE")
                            break
                    except:
                        archivo.write(paquete)

                    if primero:
                        ti = sw.start()
                        primero = False
                    paquete = client_socket.recvfrom(PAYLOAD)[0]
                tf = sw.end()
                archivo.close()

                print("El archivo se ha recibido satisfactoriamente.")
                tamanio = os.path.getsize(nombre_archivo)
                tiempo = sw.dar_duracion(ti, tf)
                logging.info(f"Entrega exitosa \
                                  \n Se recibió el archivo: {nombre_archivo} de tamaño: {tamanio} bytes \
                                  \n Recibido por el cliente {numero_cliente} \
                                  \n {tiempo}")
                break

    except Exception as e:
        print(e)
        logging.info("Entrega no exitosa")
    client_socket.close()
