from abc import ABC, abstractmethod

from commands.payload import Payload


class FrameCommand(ABC):
    """An abstract base class for commands"""

    @property
    def is_on(self):
        return self._is_on

    @is_on.setter
    def is_on(self, value):
        if self._is_on != value:
            self._is_on = value
            self._is_on_changed(value)

    def __init__(self, toggle_key):
        """"""
        super().__init__()
        self.toggle_key = toggle_key
        self._is_on = True

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def execute(self, payload: Payload) -> Payload:
        if payload.key_pressed == self.toggle_key:
            self.is_on = not self._is_on

        if self._is_on:
            payload = self._execute(payload)

        return payload

    @abstractmethod
    def _execute(self, payload: Payload) -> Payload:
        pass

    def _is_on_changed(self, is_on):
        pass
