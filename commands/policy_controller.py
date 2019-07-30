from abc import ABC, abstractmethod

from commands.abstract_command import FrameCommand
from commands.payload import Payload


class PolicyController(ABC):
    """A class for controlling the policy for a command"""

    def __init__(self):
        """"""
        super().__init__()

    def __repr__(self):
        return super().__repr__()

    @abstractmethod
    def apply(self, command, payload):
        pass


class EveryNFramesPolicy(PolicyController):

    def __init__(self, n):
        super().__init__()
        self.n = n

    def apply(self, command: FrameCommand, payload: Payload):
        command.is_on = payload.i_frame % self.n == 0

class AutoTurnOffPolicy(PolicyController):

    def __init__(self):
        super().__init__()

    def apply(self, command: FrameCommand, payload: Payload):
        command.is_on = False
