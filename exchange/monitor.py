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
cabecalho = {}


class Monitor:
    """
        Sala monitor
    """

    def __init__(self, sala_id_list, port_list=None, username='Guest'):
        """
            :param sala_id_list: lista de identificadores de sala que o monitor deseja acompanhar
            :param port_list: (opcional) lista de portas para um monitor existente
            :param username: (opcional) subscriber's username
        """
        self._id = -1

        self._dict =  {}    # Contém todas as informações de salas inscritas
        self._context = zmq.Context()

        self._socket = self._context.socket(zmq.SUB)
        self._username = username
        
        if port_list is None:
            # Rotina para criar um monitor

            # Request-reply para criar um monitor
            _socket_register_monitor = self._context.socket(zmq.REQ)
            _socket_register_monitor.connect("tcp://%s:%s" % (ADDR, SYSTEM_CREATE_MONITOR))

            # Request-reply para obter todas as relações de porta da sala-sensor
            _socket_world = self._context.socket(zmq.REQ)
            _socket_world.connect("tcp://%s:%s" % (ADDR, SYSTEM_LISTEN_PORT))

            _socket_world.send_multipart([sid.encode() for sid in sala_id_list])
            self._ports = _socket_world.recv_json()

            if 'error' not in self._ports:
                # Existe pelo menos uma porta registrada
                ordered_ids = list(self._ports.keys())
                ordered_ids.sort()
                self._monitor_id = "_".join(ordered_ids)

                # Registrar um monitor no sistema
                _socket_register_monitor.send_string(self._monitor_id)
                
                for _, port in self._ports.items():
                    self._socket.connect("tcp://%s:%s" % (ADDR, port))

                # Inscrever-se para todos os IDs de sala
                for sala_id in ordered_ids:
                    self._socket.setsockopt_string(zmq.SUBSCRIBE, sala_id)
                    self._dict[sala_id] = {
                        "data": None,           # sala object
                        "old": None,            # valor antigo
                        "variation": None       # Variação
                    }
            else:
                # Nenhuma das portas inscritas existe
                print("[MNT] Room don't exist :(")

        else:
            # Rotina para reutilizar um monitor existente
            # (usa a mesma relação de porta sala-sensor)

            self._ports = port_list
            for port in port_list:
                self._socket.connect("tcp://%s:%s" % (ADDR, port))
            
            # Inscrever-se para todos os IDs de sala
            for sala_id in sala_id_list:
                self._socket.setsockopt_string(zmq.SUBSCRIBE, sala_id)
                self._dict[sala_id] = {
                    "data": None,
                    "old": None,
                    "variation": None
                }

    def _update_sala(self, obj):
        """
            Create/Updates uma sala existente
            :param obj: Sala object (ou una lista de salas)
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
            Main loop para monitorar atualizações das salas
        """

        if self._dict:
            print("Listening...")
            while True:
                [_id, d_sala] = self._socket.recv_multipart()
                sala = create_sala_json(unmarshal(d_sala))
                sala_id = _id.decode()
                self._update_sala(sala)
                
                # Visualização de atualizações
                self.show_in_terminal()

    def show_in_terminal(self):
        """
            Visualização atualizações no console
        """
        global lista_salas
        global cabecalho

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

                file2write=open(key,'a')

                if key not in cabecalho:
                    cabecalho.setdefault(key, False)

                if cabecalho[key] == False:
                    file2write.write("-"*no_dash)
                    file2write.write("\n")
                    file2write.write("NOME\t   TEMP \t   VAR\t\tMÉDIA\t\tDATA\n")
                    file2write.write("-"*no_dash)
                    file2write.write("\n")
                    cabecalho[key] = True

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
                        file2write.write("%s\t %.2f ºC\t %2.2f%% ºC \t %2.2fºC \t" % (key, value['data'].get_value(), value['variation'], media) + str(dateTimeObj) + "\n")
                    else:
                        print("%s\t %.2f ºC\t %2.2f%% ºC" % (key, value['data'].get_value(), value['variation']))

                else:
                    l2 = len("+%.2f%%" % value['variation'])
                    _white_space = no_dash - l1 - len(key) - 13 - l2
                    if len(lista_salas[key]) == 10:
                        print("%s\t %.2f ºC\t +%2.2f%% ºC \t %2.2fºC \t" % (key, value['data'].get_value(), value['variation'], media) + str(dateTimeObj))
                        file2write.write("%s\t %.2f ºC\t +%2.2f%% ºC \t %2.2fºC \t" % (key, value['data'].get_value(), value['variation'], media) + str(dateTimeObj) + "\n")
                    else:
                        print("%s\t %.2f ºC\t +%2.2f%% ºC" % (key, value['data'].get_value(), value['variation']))

        print()

    def get_dict(self):
        return self._dict
