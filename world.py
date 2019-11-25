# -*- coding: utf-8 -*-
from exchange.broker import Broker
from config import (ADDR, SYSTEM_LISTEN_PORT, SYSTEM_UPDATE_PORT, SYSTEM_CREATE_MONITOR, SYSTEM_EXISTS_MONITOR, SENSOR_01, SENSOR_20)
from threading import Thread
import zmq, json

"""
To run this code use:

python3 world.py

"""

class SalaSystem:
    """
        Main system
        Runs a Broker;
        Manages sala-sensor port relations;
        Manages existing monitors
    """
    def __init__(self):
        self._bkr = Broker()        # Broker object
        self._sala_port = {}         # sala-sensor port relations
        self._monitors = {}         # Created monitors and it's subscribed woker ports

        self._context = zmq.Context()
        
        # Request-reply for update sala-sensor port relations
        self._socket_update = self._context.socket(zmq.REP)
        self._socket_update.bind("tcp://%s:%s" % (ADDR, SYSTEM_UPDATE_PORT))

        # Request-reply for getting all sala-sensor port relations
        self._socket_listen = self._context.socket(zmq.REP)
        self._socket_listen.bind("tcp://%s:%s" % (ADDR, SYSTEM_LISTEN_PORT))


        self._sensor_ports = range(SENSOR_01, SENSOR_20)    # All possible sensor ports
        self._sensor_index = 0

        # Request-reply for creating and registrating a monitor
        self._socket_create_monitor = self._context.socket(zmq.REP)
        self._socket_create_monitor.bind("tcp://%s:%s" % (ADDR, SYSTEM_CREATE_MONITOR))

        # Request-reply for informing if a given monitor already exists
        self._socket_exists_monitor = self._context.socket(zmq.REP)
        self._socket_exists_monitor.bind("tcp://%s:%s" % (ADDR, SYSTEM_EXISTS_MONITOR))

    # Verify if it already exists a similar monitor and reuses it
    def _exists_monitor(self):
        while True:
            monitor_id = self._socket_exists_monitor.recv_string()
            if monitor_id in self._monitors:
                self._socket_exists_monitor.send_json({monitor_id: self._monitors[monitor_id]})
            else:
                self._socket_exists_monitor.send_json({"error": "Monitor does not exists"})

    # Create a new monitor with the specified sala list and the correct sensor port
    def _create_monitor(self):
        while True:
            monitor_id = self._socket_create_monitor.recv_string()
            sensores_port = []
            sala_id_list = monitor_id.split("_")
            if monitor_id not in self._monitors:
                for key in sala_id_list:
                    sensores_port.append(self._sala_port[key])
                self._monitors[monitor_id] = sensores_port
                self._socket_create_monitor.send_json({"success": "Monitor Created"})

    # Gives a port to a new sensor
    def _update(self):
        while True:
            sala_id = self._socket_update.recv_string()
            new_port = self._sensor_ports[self._sensor_index]
            self._sensor_index += 1
            self._sala_port[sala_id] = new_port

            print("[UPD]", self._sala_port)

            self._socket_update.send_string(str(new_port))
            
    # Gives the correct port for each specified sala 
    def _listen(self):
        while True:
            raw_data = self._socket_listen.recv_multipart()
            ports = {}
            for sala_id in raw_data:
                if sala_id.decode() in self._sala_port:
                    ports[sala_id.decode()] = self._sala_port[sala_id.decode()]

            print("[LST]", self._sala_port)

            if ports:
                self._socket_listen.send_json(ports)
            else:
                self._socket_listen.send_json({'error': 'sala not found'})

    # Each world action is running in a thread
    def start(self):
        thr_update_port = Thread(target=self._update)
        thr_listen_port = Thread(target=self._listen)

        thr_create_monitor = Thread(target=self._create_monitor)
        thr_exists_monitor = Thread(target=self._exists_monitor)

        thr_update_port.start()
        thr_listen_port.start()

        thr_create_monitor.start()
        thr_exists_monitor.start()

        self._bkr.start()

        thr_update_port.join()
        thr_listen_port.join()

def main():
    system = SalaSystem()
    system.start()

if __name__ == "__main__":
    main()
