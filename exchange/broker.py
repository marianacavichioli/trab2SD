# -*- coding: utf-8 -*-

import time
import zmq
import pdb
from zmq.devices.basedevice import ProcessDevice
from multiprocessing import Process
from config import (BROKER_IN_PORT, BROKER_OUT_PORT, ADDR)

class Broker:
    """
        Broker device for distributing manager messages to their sensors
        'device' on https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/pyzmqdevices/streamer.html
    """
    def __init__(self):
        self._context = zmq.Context(1)
        # Socket facing clients
        # MANAGER -> BROKER (input)
        self._frontend = self._context.socket(zmq.PULL)
        self._frontend.bind("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))
        
        # Socket facing services
        # BROKER (output) -> SENSOR
        self._backend = self._context.socket(zmq.PUB)
        self._backend.bind("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))

    def start(self):
        """
            Start device
        """
        zmq.device(zmq.STREAMER, self._frontend, self._backend)
    
    def __del__(self):
        self._frontend.close()
        self._backend.close()
        self._context.term()

