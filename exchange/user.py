# -*- coding: utf-8 -*-

import zmq
import time
from config import (ADDR, BROKER_IN_PORT, SYSTEM_EXISTS_MONITOR)
from exchange.monitor import Monitor
from exchange.sala import Sala
from exchange.sensor import Sensor


class Subscriber:
    """
        Cliente que monitora salas
        Todo subscriber possui um monitor e apenas um
    """
    def __init__(self, username=None, sala_id_list=None):
        """
            :param sala_id_list: lista de IDs de sala que este cliente deseja de inscrever
        """
        self._id_list = sala_id_list
        self._username = username
        self._context = zmq.Context()

        # Verifica se o monitor existe
        _socket_exists_monitor = self._context.socket(zmq.REQ)
        _socket_exists_monitor.connect("tcp://%s:%s" % (ADDR, SYSTEM_EXISTS_MONITOR))
        sala_id_list.sort()

        _key = "_".join(sala_id_list)
        _socket_exists_monitor.send_string(_key)
        response_json = _socket_exists_monitor.recv_json()

        if not "error" in response_json:
            print("[SUB] Monitor exists")
            response_sala_id_list = list(response_json.keys())[0].split("_")
            self._monitor = Monitor(sala_id_list=response_sala_id_list, port_list=response_json[_key], username=self._username)
        else:
            print("[SUB] Creating monitor")
            self._monitor = Monitor(sala_id_list=sala_id_list, username=self._username)

    def listen(self):
        """
            Iniciar visualização do monitor
        """
        self._monitor.listen()


class Manager:
    """
        Gerente de Sala.
        Todo manager de sala gerencia uma sala e apenas uma
    """
    def __init__(self, sala_name, sala_id, sala_val):
        """
            :param sala_val: Valor atual de uma sala em ºC
        """
        self._my_sala = Sala(name=sala_name, id_sala=sala_id, val=sala_val)
        self._context = zmq.Context()

        # Conexão do pipeline ao lado de entrada do broker (back-end)
        self._socket = self._context.socket(zmq.PUSH)
        self._socket.connect("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))

    def update_value(self, sala_value):
        """
            Atualize o valor atual da sala deste manager
            : param sala_value: novo valor para uma sala
        """
        self._my_sala.set_value(sala_value)

    def get_curr_value(self):
        """
            Obter o valor atual da sala
        """
        return self._my_sala.get_value()

    def send_sala(self):
        """
            Envia sala para o broker
        """
        self._socket.send_multipart(
            [str(self._my_sala.get_id()).encode(), self._my_sala.marshal()]
            )
