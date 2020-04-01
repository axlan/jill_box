#!/usr/bin/env python3

# NOTE: NEEDS SYNCHRONIZATION FOR MULTITHREADING

import random
import string
from enum import Enum, auto
from abc import ABC,abstractmethod 

from typing import (
    Dict,
    List,
    Optional,
    Tuple
)

def _random_id() -> str:
    ascii = string.ascii_lowercase
    return "".join(random.choices(ascii, k=GameGateway.NUM_ROOM_LETTERS))

class JoinReturnCodes(Enum):
    SUCCESS = auto()
    NAME_IN_USE = auto()
    ROOM_NOT_FOUND = auto()

class GetReturnCodes(Enum):
    SUCCESS = auto()
    ROOM_NOT_FOUND = auto()
    NAME_NOT_FOUND = auto()

class StartReturnCodes(Enum):
    SUCCESS = auto()
    TOO_FEW_PLAYERS = auto()
    ALREADY_STARTED = auto()
    ROOM_NOT_FOUND = auto()

class InteractReturnCodes(Enum):
    SUCCESS = auto()
    INVALID_DATA = auto()
    WRONG_STATE = auto()
    ROOM_NOT_FOUND = auto()
    PLAYER_NOT_FOUND = auto()


class Player:
    def __init__(self):
        pass

class Room(ABC):
    def __init__(self):
        self.players: Dict[str, Player] = {}
    def add_player(self, name) -> bool:
        if name in self.players.keys():
            return False
        self.players[name] = Player()
        return True
    @abstractmethod
    def start(self) -> StartReturnCodes:
        pass
    @abstractmethod
    def get_room_state(self, player) -> Tuple[InteractReturnCodes, str]:
        pass
    @abstractmethod
    def submit_data(self, player, data) -> InteractReturnCodes:
        pass

class GameGateway:

    NUM_ROOM_LETTERS = 4

    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def room_start(self, room) -> StartReturnCodes:
        if room not in self.rooms:
            return StartReturnCodes.ROOM_NOT_FOUND
        return self.rooms[room].start()

    def new_game(self, room_class) -> str:
        room = _random_id()
        self.rooms[room] = room_class()
        return room

    def join_room(self, room, name) -> JoinReturnCodes:
        try:
            success = self.rooms[room].add_player(name)
            if success:
                return JoinReturnCodes.SUCCESS
            else:
                return JoinReturnCodes.NAME_IN_USE
        except:
            return JoinReturnCodes.ROOM_NOT_FOUND

    def get_room_state(self, room, name=None) -> Tuple[InteractReturnCodes, str]:
        if room in self.rooms:
            if name is None or name in self.rooms[room].players:
                return self.rooms[room].get_room_state(name)
            else:
                return (InteractReturnCodes.PLAYER_NOT_FOUND, '')
        return (InteractReturnCodes.ROOM_NOT_FOUND, '')

    def submit_data(self, room, name, data) -> InteractReturnCodes:
        if room in self.rooms:
            if name in self.rooms[room].players:
                return self.rooms[room].submit_data(name, data)
            else:
                return InteractReturnCodes.PLAYER_NOT_FOUND
        return InteractReturnCodes.ROOM_NOT_FOUND
