from abc import ABC, abstractmethod

from commands.abstract_command import FrameCommand
from commands.payload import Payload
from common.exceptions import ArgumentException


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


class EveryNSecondsPolicy(PolicyController):

    def __init__(self, n: float) -> None:
        super().__init__()
        self.n = n

    def apply(self, command: FrameCommand, payload: Payload):
        is_on =(payload.elapsed) % self.n == 0
        command.is_on = is_on


class AutoTurnOffPolicy(PolicyController):

    def __init__(self):
        super().__init__()

    def apply(self, command: FrameCommand, payload: Payload):
        command.is_on = False


class DelayedStartPolicy(PolicyController):

    def __init__(self, n_seconds=None, n_frames=None):
        super().__init__()
        valid = True
        if n_seconds and n_frames:
            valid = False
        if not (n_seconds or n_frames):
            valid = False
        if not valid:
            raise ArgumentException('Exactly 1 of frames / seconds delay should be specified')

        self.trace_frames = n_frames is not None
        self.n_seconds = n_seconds
        self.n_frames = n_frames

    def apply(self, command: FrameCommand, payload: Payload):
        if self.trace_frames:
            is_on = payload.i_frame >= self.n_frames
        else:
            is_on = payload.elapsed >= self.n_seconds

        command.is_on = is_on
