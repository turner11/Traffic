from abc import ABC, abstractmethod
from collections import defaultdict
from enum import IntEnum
from typing import List, Dict
from commands.abstract_command import FrameCommand

# We need to make sure they were loaded...
# noinspection PyCompatibility
from commands import *


def _get_commands_by_type() -> Dict[IntEnum, List[FrameCommand]]:
    commands_by_type = defaultdict(list)
    for cmd in FrameCommand.get_all_commands():
        commands_by_type[cmd.get_layer_type()].append(cmd)

    return commands_by_type


class PipeLineBuilder(ABC):
    """"""

    _commands_by_type: Dict[IntEnum, List[FrameCommand]] = _get_commands_by_type()

    def __init__(self):
        """"""
        super().__init__()

    def __repr__(self):
        return super().__repr__()

    @abstractmethod
    def get_raw_data_processing_commands(self) -> List[FrameCommand]:
        pass

    @abstractmethod
    def get_augmentation_commands(self) -> List[FrameCommand]:
        pass

    @abstractmethod
    def get_out_put_commands(self) -> List[FrameCommand]:
        pass

    @classmethod
    def _enum_to_commands(cls, commands_enum):
        types = cls._commands_by_type[commands_enum]
        instances = [ctor() for ctor in types]
        return instances
