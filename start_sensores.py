#-*- coding: utf-8 -*-
from exchange.sensor import Sensor
from threading import Thread

"""
To run this code use:

python3 start_sensores.py

"""

def main():
    # Each sala has a sensor 
    # Creating sensores for our examples
    sensor_le1 = Sensor("LE1")
    sensor_le2 = Sensor("LE2")
    sensor_le3 = Sensor("LE3")
    sensor_le4 = Sensor("LE4")
    sensor_le5 = Sensor("LE5")
    sensor_le6 = Sensor("LE6")
    sensor_le7 = Sensor("LE7")
    sensor_le8 = Sensor("LE8")

    # Each sensor will be running in a thread
    thread_LE1 = Thread(target=sensor_le1.work)
    thread_LE2 = Thread(target=sensor_le2.work)
    thread_LE3 = Thread(target=sensor_le3.work)
    thread_LE4 = Thread(target=sensor_le4.work)
    thread_LE5 = Thread(target=sensor_le5.work)
    thread_LE6 = Thread(target=sensor_le6.work)
    thread_LE7 = Thread(target=sensor_le7.work)
    thread_LE8 = Thread(target=sensor_le8.work)

    thread_LE1.start()
    thread_LE2.start()
    thread_LE3.start()
    thread_LE4.start()
    thread_LE5.start()
    thread_LE6.start()
    thread_LE7.start()
    thread_LE8.start()

    thread_LE1.join()
    thread_LE2.join()
    thread_LE3.join()
    thread_LE4.join()
    thread_LE5.join()
    thread_LE6.join()
    thread_LE7.join()
    thread_LE8.join()


if __name__ == "__main__":
    main()