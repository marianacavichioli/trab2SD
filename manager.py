# -*- coding: utf-8 -*-

from exchange.user import Manager
from sys import argv
import random 
from random import randint
from time import sleep
from threading import Thread


# Função que atualiza o valor do manager aleatoriamente com um valor entre -0.1 e 0.1
def modify_value(manager):
    if isinstance(manager, Manager):
        while True:
            manager.send_sala()
            sleep(randint(1,5))
            manager.update_value(
                manager.get_curr_value() + random.uniform(-0.1, 0.1)
            )

def main(item):
    # Criando exemplos de salas
    sala_le1 = Manager("Laboratório Educacional 1", "LE1", 23)
    sala_le2 = Manager("Laboratório Educacional 2", "LE2", 22)
    sala_le3 = Manager("Laboratório Educacional 3", "LE3", 20)
    sala_le4 = Manager("Laboratório Educacional 4", "LE4", 26)
    sala_le5 = Manager("Laboratório Educacional 5", "LE5", 30)
    sala_le6 = Manager("Laboratório Educacional 6", "LE6", 32)
    sala_le7 = Manager("Laboratório Educacional 7", "LE7", 18)
    sala_le8 = Manager("Laboratório Educacional 8", "LE8", 21)

    # Cada sala será constantemente atualizada em uma thread
    thread_le1 = Thread(target=modify_value, args=(sala_le1,))
    thread_le2 = Thread(target=modify_value, args=(sala_le2,))
    thread_le3 = Thread(target=modify_value, args=(sala_le3,))
    thread_le4 = Thread(target=modify_value, args=(sala_le4,))
    thread_le5 = Thread(target=modify_value, args=(sala_le5,))
    thread_le6 = Thread(target=modify_value, args=(sala_le6,))
    thread_le7 = Thread(target=modify_value, args=(sala_le7,))
    thread_le8 = Thread(target=modify_value, args=(sala_le8,))
    

    thread_le1.start()
    thread_le2.start()
    thread_le3.start()
    thread_le4.start()
    thread_le5.start()
    thread_le6.start()
    thread_le7.start()
    thread_le8.start()

    thread_le1.join()
    thread_le2.join()
    thread_le3.join()
    thread_le4.join()
    thread_le5.join()
    thread_le6.join()
    thread_le7.join()
    thread_le8.join()

if __name__ == "__main__":
    main(argv)
