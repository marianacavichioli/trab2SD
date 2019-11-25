# -*- coding: utf-8 -*-

import zmq
import time
from config import (ADDR, BROKER_IN_PORT, SYSTEM_EXISTS_MONITOR)
from exchange.monitor import Monitor
from exchange.sala import Sala
from exchange.sensor import Sensor


class Subscriber:
    """
        Client that monitors salas
        Every subscriber has one monitor and one only
    """
    def __init__(self, username=None, sala_id_list=None):
        """
            :param sala_id_list: list of sala IDs that this client wants to subscribe for
        """
        self._id_list = sala_id_list
        self._username = username
        self._context = zmq.Context()

        # Verify if a monitor exists
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
            Start monitor visualization
        """
        self._monitor.listen()


class Manager:
    """
        Sala manager.
        Every sala manager manages one sala and one only
    """
    def __init__(self, sala_name, sala_id, sala_val):
        """
            :param sala_val: Current value of a sala in dollars
        """
        self._my_sala = Sala(name=sala_name, id_sala=sala_id, val=sala_val)
        self._context = zmq.Context()

        # Pipeline connection to broker's input side (backend)
        self._socket = self._context.socket(zmq.PUSH)
        self._socket.connect("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))

    def update_value(self, sala_value):
        """
            Update the current value of this manager's sala
            :param sala_value: new value for a sala
        """
        self._my_sala.set_value(sala_value)

    def get_curr_value(self):
        """
            Get sala's current value
        """
        return self._my_sala.get_value()

    def send_sala(self):
        """
            Send sala to broker
        """
        self._socket.send_multipart(
            [str(self._my_sala.get_id()).encode(), self._my_sala.marshal()]
            )
