import threading
import logging
from datetime import datetime

now = datetime.now()  # current date and time
now_str = now.strftime("%Y-%m-%d-%I-%M-%S")

num_conexiones = int(input("¿Cuántas conexiones desea realizar al servidor?"))

logging.basicConfig(filename=f'./Logs/{now_str}-log.txt', filemode='w',
                    encoding='utf-8', datefmt='', level=logging.INFO)
