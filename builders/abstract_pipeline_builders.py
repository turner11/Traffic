from abc import ABC, abstractmethod
from typing import List
from commands.abstract_command import FrameCommand


class PipeLineBuilder(ABC):
    """"""

    def __init__(self):
        """"""
        super().__init__()

    def __repr__(self):
        return super().__repr__()

    @abstractmethod
    def get_commands(self) -> List[FrameCommand]:
        pass


class RunTimePipelineBuilder(PipeLineBuilder):
    """"""

    def __init__(self, commands: List[FrameCommand] = None):
        """"""

        super().__init__()
        self._commands = commands

    def __repr__(self):
        return f'{self.__class__.__name__}({self._commands}'

    def get_commands(self) -> List[FrameCommand]:
        return self._commands[:]
