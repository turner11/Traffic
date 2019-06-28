from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Type


class FrameCommand(ABC):
    """An abstract base class for commands"""

    def __init__(self):
        """"""
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    @abstractmethod
    def execute(self, frame_container):
        pass

    @classmethod
    @abstractmethod
    def get_layer_type(cls) -> IntEnum:
        pass

    @staticmethod
    def get_all_commands():
        yield from FrameCommand.get_subclasses()

    @classmethod
    def get_subclasses(cls):
        subclass: Type[FrameCommand]
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass
