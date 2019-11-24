# -*- coding: utf-8 -*-

from json import (dumps, loads)

def create_sala_json(json):
    """
        Converts a JSON representation to a Sala object
    """
    return Sala(
        name=json["name"],
        id_sala=json["id"],
        val=json["value"]
    )

def marshal(sala):
    """
        Transforms an object into a byte JSON representation
        :param sala: Representation of a room
    """
    if isinstance(sala, Sala):
        return marshal({
            "id": sala.get_id(),
            "name": sala.get_name(),
            "value": sala.get_value()
        })
    elif isinstance(sala, dict):
        return dumps(sala).encode()

def unmarshal(d_json):
    """
        Transforms an a byte JSON representation into a JSON representation
        :param sala: Representation of a room
    """
    if isinstance(d_json, str):
        return loads(d_json)
    elif isinstance(d_json, bytes):
        return unmarshal(d_json.decode())

class Sala:
    """
        Sala object
    """
    def __init__(self, name, id_sala, val):
        """
            :param id_sala: room identifier
            :param name: room name
            :param val: Initial room value
        """
        self._id = id_sala
        self._name = name
        self._val = val

    # Getters
    def get_name(self):
        return self._name

    def get_value(self):
        return self._val

    def set_value(self, new_value):
        self._val = new_value

    def get_id(self):
        return self._id

    def marshal(self):
        """
            Transforms this room to to a byte JSON representation
        """
        return marshal(self)

    def __repr__(self):
        return "<Sala %r>" % self._name
