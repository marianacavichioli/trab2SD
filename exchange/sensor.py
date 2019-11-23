# -*- coding: utf-8 -*-
import json
import time
import zmq
import random
import sys
from threading import Thread
from exchange.sala import (marshal, unmarshal, create_sala_json)
from config import (ADDR, BROKER_OUT_PORT, SYSTEM_UPDATE_PORT)

class Sensor:
    """
        Sensor object
        Every sensor has one sala and one only
    """
    def __init__(self, sala_id=None):
        """
            :param sala_id: sala id to be responsible with
        """
        self._sensor_id = random.randrange(1,10005)

        # BROKER -> SENSOR
        self._context = zmq.Context()

        # Subscribe to a sala
        self._socket_in = self._context.socket(zmq.SUB)
        self._socket_in.connect("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))
        self._socket_in.setsockopt_string(zmq.SUBSCRIBE, sala_id)
        
        # Request-reply to give this sensor a port
        _socket_world = self._context.socket(zmq.REQ)
        _socket_world.connect("tcp://%s:%s" % (ADDR, SYSTEM_UPDATE_PORT))

        _socket_world.send_string(sala_id)
        self._my_port = _socket_world.recv_string()

        # Publishes a sala for monitors
        self._socket_out = self._context.socket(zmq.PUB)
        self._socket_out.bind("tcp://%s:%s" % (ADDR, self._my_port))

        self._sala = None

    def _listen(self):
        """
            Receive sala updates
        """
        while True:
            [_, raw_data] = self._socket_in.recv_multipart()
            data = unmarshal(raw_data.decode())

            print("[WKR] Sensor %s received %r" % (self._sensor_id, data))
            self._sala = create_sala_json(data)

    def _update(self):
        """
            Send sala current state each at second
        """
        while True:
            if self._sala is not None:
                self._socket_out.send_multipart(
                    [str(self._sala.get_id()).encode(), marshal(self._sala)]
                )
            time.sleep(1)

    def work(self):
        """
            Main loop for running this sensor
        """
        update_thr = Thread(target=self._update)

        update_thr.start()
        self._listen()

        update_thr.join()

        

        

        
      
