# Script para el cliente

import socket
import logging
import os
import stopwatch as sw
import hashlib

LISTO = 'LISTO'
ULTIMO_PAQUETE = 'ULTIMO_PAQUETE'
TAMANIO_CHUNK = 4096

ip = '192.168.146.128'
#ip = '127.0.0.1'


def crear_conexion(numero_cliente: int, cantidad_conexiones: int):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Cambiar al puerto 20 en produccion
        client_socket.connect((ip, 21))
        print(f"Conexión exitosa cliente {numero_cliente}")
        logging.info(f"Conexión hecha para cliente {numero_cliente}")
    except:
        print("Conexión no exitosa. Vuelva a intentarlo.")
    try:
        while True:
            client_socket.send(f'{numero_cliente}'.encode('utf-8'))
            listo = input(
                f"¿Está listo para recibir el archivo cliente {numero_cliente}? Escriba 's' si lo está y algo más de lo contrario: ")

            if listo == 's':

                nombre_archivo = f"./ArchivosRecibidos/Cliente{numero_cliente}-Prueba{cantidad_conexiones}.txt"
                client_socket.send(LISTO.encode('utf-8'))
                archivo = open(nombre_archivo, "wb+")

                primero = True
                chunk = client_socket.recv(TAMANIO_CHUNK)
                while True:

                    try:
                        if chunk.decode('utf-8') == 'DONE':
                            print("Se recibe un DONE")
                            break
                    except:
                        archivo.write(chunk)

                    if primero:
                        ti = sw.start()
                        primero = False
                    chunk = client_socket.recv(TAMANIO_CHUNK)
                tf = sw.end()
                archivo.close()

                client_socket.send(ULTIMO_PAQUETE.encode('utf-8'))

                hash_recibido = client_socket.recv(TAMANIO_CHUNK)
                hash_valido = validar_hash(nombre_archivo, hash_recibido)

                if hash_valido:
                    print("El archivo se ha recibido satisfactoriamente.")
                    tamanio = os.path.getsize(nombre_archivo)
                    tiempo = sw.dar_duracion(ti, tf)
                    logging.info(f"Entrega exitosa \
                                  \n Se recibió el archivo: {nombre_archivo} de tamaño: {tamanio} bytes \
                                  \n Recibido por el cliente {numero_cliente} \
                                  \n {tiempo}")
                    break
                else:
                    os.remove(nombre_archivo)
                    print("¡El archivo ha sido alterado!")
                    logging.info(
                        f"Entrega no exitosa para el cliente {numero_cliente}")

    except KeyboardInterrupt:
        print("Salida por usuario")
    client_socket.close()


def validar_hash(archivo, hash_recibido) -> bool:
    with open(archivo, "rb") as f:
        calculado = hashlib.sha256(f.read()).digest()
        return calculado == hash_recibido
