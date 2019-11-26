# -*- coding: utf-8 -*-

import json
from exchange.sala import Sala

"""
    Constantes usadas no projeto
    MANAGER -> BROKER -> SENSORES -> MONITOR -> SUBSCRIBER
"""

ADDR = '127.0.0.1'

SENSOR_01 = 9100    # Primeira porta reservada para os sensores
SENSOR_20 = 9120    # Última porta reservada para os sensores

BROKER_IN_PORT      =   '9630'  # Porta de entrada do Broker
BROKER_OUT_PORT     =   '9031'  # Porta de saída do Broker

SYSTEM_EXISTS_MONITOR = '9896'  # Porta para checar se o monitor existe
SYSTEM_CREATE_MONITOR = '9897'  # Porta para registrar um novo monitor

SYSTEM_UPDATE_PORT    = '9898'  # Porta para atualizar a relação sala-sensor
SYSTEM_LISTEN_PORT    = '9899'  # Porta para requisição de todas as relações sala-sensor
