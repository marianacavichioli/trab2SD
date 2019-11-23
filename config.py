# -*- coding: utf-8 -*-

import json
from exchange.sala import Sala

"""
    Constants used in this project
    MANAGER -> BROKER -> SENSORES -> MONITOR -> SUBSCRIBER
"""

# IP Address for running the system.
ADDR = '127.0.0.1'

SENSOR_01 = 9100    # First reserved port for sensores
SENSOR_20 = 9120    # Last reserved port for sensores

BROKER_IN_PORT      =   '9630'  # Broker input (frontend) port
BROKER_OUT_PORT     =   '9031'  # Broker output (backend) port

SYSTEM_EXISTS_MONITOR = '9896'  # Port for checking if a given monitor exists
SYSTEM_CREATE_MONITOR = '9897'  # Port for register a new model

SYSTEM_UPDATE_PORT    = '9898'  # Port for updating sala-sensor relation
SYSTEM_LISTEN_PORT    = '9899'  # Port for requesting all sala-sensor relation
