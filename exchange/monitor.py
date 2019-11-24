# -*- coding: utf-8 -*-

import zmq
import json
from exchange.sala import (Sala, create_sala_json, unmarshal)
from config import (ADDR, SYSTEM_LISTEN_PORT, SYSTEM_CREATE_MONITOR)
import random
import os
import signal
from datetime import datetime

lista_salas = {}


class Monitor:
    """
        Sala monitor
    """

    def __init__(self, sala_id_list, port_list=None, username='Guest'):
        """
            :param sala_id_list: list of sala identifiers the monitor wants to keep track
            :param port_list: (optional) list of ports for an existing monitor
            :param username: (optional) subscriber's username
        """
        self._id = -1

        self._dict =  {}    # Contains all subscribed salas informations
        self._context = zmq.Context()

        # Monitor subscribing to broker's backend
        self._socket = self._context.socket(zmq.SUB)
        self._username = username
        
        if port_list is None:
            # Routine for creating a monitor

            # Request-reply for creating a monitor
            _socket_register_monitor = self._context.socket(zmq.REQ)
            _socket_register_monitor.connect("tcp://%s:%s" % (ADDR, SYSTEM_CREATE_MONITOR))

            # Request-reply for getting all sala-sensor port relations
            _socket_world = self._context.socket(zmq.REQ)
            _socket_world.connect("tcp://%s:%s" % (ADDR, SYSTEM_LISTEN_PORT))

            _socket_world.send_multipart([sid.encode() for sid in sala_id_list])
            self._ports = _socket_world.recv_json()

            if 'error' not in self._ports:
                # At least one subscribed port exists
                ordered_ids = list(self._ports.keys())
                ordered_ids.sort()
                self._monitor_id = "_".join(ordered_ids)

                # Register a monitor to system
                _socket_register_monitor.send_string(self._monitor_id)
                
                for _, port in self._ports.items():
                    self._socket.connect("tcp://%s:%s" % (ADDR, port))

                # Subscribe to all sala IDs
                for sala_id in ordered_ids:
                    self._socket.setsockopt_string(zmq.SUBSCRIBE, sala_id)
                    self._dict[sala_id] = {
                        "data": None,           # sala object
                        "old": None,            # Old value
                        "variation": None          # Variation in %
                    }
            else:
                # Neither of the subscribed ports exists
                print("[MNT] Sala don't exist :(")

        else:
            # Routine for reusing an existing monitor
            # (uses the same sala-sensor port relation)

            self._ports = port_list
            for port in port_list:
                self._socket.connect("tcp://%s:%s" % (ADDR, port))
            
            # Subscribe to all sala IDs
            for sala_id in sala_id_list:
                self._socket.setsockopt_string(zmq.SUBSCRIBE, sala_id)
                self._dict[sala_id] = {
                    "data": None,
                    "old": None,
                    "variation": None
                }

    def _update_sala(self, obj):
        """
            Create/Updates an existing sala
            :param obj: Sala object (or a list of sala)
        """
        if isinstance(obj, list):
            for sala in obj:
                self._update_sala(sala)

        if isinstance(obj, Sala):
            if self._dict[obj.get_id()]['data'] is None:
                self._dict[obj.get_id()]['data'] = obj
            else:
                old_val = self._dict[obj.get_id()]['data'].get_value()
                variation = (obj.get_value() - old_val)*100 / old_val
                self._dict[obj.get_id()]['data'] = obj
                self._dict[obj.get_id()]['old'] = old_val
                if variation != 0:
                    self._dict[obj.get_id()]['variation'] = variation

    def listen(self):
        """
            Main loop of listening salas updates
        """

        if self._dict:
            print("Listening...")
            while True:
                [_id, d_sala] = self._socket.recv_multipart()
                sala = create_sala_json(unmarshal(d_sala))
                sala_id = _id.decode()
                self._update_sala(sala)
                
                # Visualize updates
                self.show_in_terminal()

    def show_in_terminal(self):
        """
            Visualize updates on console
        """
        global lista_salas

        

        no_dash = 70
        os.system('cls' if os.name == 'nt' else 'clear')
        print("USERNAME: %s" % (self._username))
        print("Monitoring: %s;" % (", ".join(list(self._dict.keys()))))
        print("-"*no_dash)
        print("NOME\t   TEMP \t   VAR\t\tMÉDIA\t\tDATA")
        print("-"*no_dash)
        for key, value in self._dict.items():
            if value['data'] and value['variation'] is not None:

                now = datetime.now()
                dateTimeObj = datetime.now()

                if key not in lista_salas:
                    lista_salas.setdefault(key, [])
        
                if len(lista_salas[key]) == 10:
                    lista_salas[key].pop(0)
                lista_salas[key].append(value['data'].get_value())
                
                media = sum(lista_salas[key])/len(lista_salas[key])

                l1 = len("%.2f ºC" %  value['data'].get_value() )
                if value['variation'] < 0:
                    l2 = len("%.2f%%" % value['variation'])
                    _white_space = no_dash - l1 - len(key) - 13 - l2
                    if len(lista_salas[key]) == 10:
                        print("%s\t %.2f ºC\t %2.2f%% ºC \t %2.2fºC \t" % (key, value['data'].get_value(), value['variation'], media) + str(dateTimeObj))
                    else:
                        print("%s\t %.2f ºC\t %2.2f%% ºC" % (key, value['data'].get_value(), value['variation']))
                else:
                    l2 = len("+%.2f%%" % value['variation'])
                    _white_space = no_dash - l1 - len(key) - 13 - l2
                    if len(lista_salas[key]) == 10:
                        print("%s\t %.2f ºC\t +%2.2f%% ºC \t %2.2fºC \t" % (key, value['data'].get_value(), value['variation'], media) + str(dateTimeObj))
                    else:
                        print("%s\t %.2f ºC\t +%2.2f%% ºC" % (key, value['data'].get_value(), value['variation']))
        print()

    def get_dict(self):
        return self._dict
