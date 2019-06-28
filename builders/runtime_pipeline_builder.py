from typing import List

from builders.pipeline_builders import PipeLineBuilder
from commands.abstract_command import FrameCommand


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
