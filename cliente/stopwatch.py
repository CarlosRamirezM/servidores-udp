#Código adaptado de https://www.codespeedy.com/how-to-create-a-stopwatch-in-python/

import time

def dar_duracion(start_time, end_time):
  sec = end_time - start_time
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("El tiempo de transferencia del archivo fue {0}h:{1}min:{2}sec".format(int(hours),int(mins),sec))

def start():
    return time.time()

def end():
    return time.time()
