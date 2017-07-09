from .heroes import Hero
from .monsters import Monster
from .exceptions import *


class Battle(object):
    def __init__(self, participants):
        """
        determines initiative order using unit speed
        """
        pass

    def current_attacker(self):
        """
        returns unit at front of initiative queue
        """
        pass

    def start(self):
        pass

    def execute_command(self, command, target):
        """
        causes current hero to execute a command on a target
        raises InvalidCommand if unit does not have that command
        raises InvalidTarget if unit is dead
        """
        pass
