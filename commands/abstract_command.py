from abc import ABC, abstractmethod


class FrameCommand(ABC):
    """An abstract base class for commands"""

    def __init__(self):
        """"""
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    @abstractmethod
    def execute(self, frame_container):
        pass
