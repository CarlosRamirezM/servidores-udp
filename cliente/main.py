from multiprocessing.connection import wait
import threading
import logging
from datetime import datetime
from time import time, sleep
from cliente import crear_conexion

now = datetime.now()  # current date and time
now_str = now.strftime("%Y-%m-%d-%I-%M-%S")

num_conexiones = int(input("¿Cuántas conexiones desea realizar al servidor? "))

logging.basicConfig(filename=f'./Logs/{now_str}-log.txt', filemode='w',
                    encoding='utf-8', datefmt='', level=logging.INFO)
logging.info("LOG INICIADO")

for i in range(1, num_conexiones+1):
    cliente = threading.Thread(
        target=crear_conexion, args=(i, num_conexiones,))
    cliente.start()
    sleep(0.2)
