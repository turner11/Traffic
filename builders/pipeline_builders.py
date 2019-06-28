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
