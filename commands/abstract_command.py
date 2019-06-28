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

    def __init__(self, toggle_key, subscribed_keys=None):
        """"""
        super().__init__()
        self.toggle_key = toggle_key
        self.subscribed_keys = subscribed_keys or []
        self._is_on = True

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def execute(self, payload: Payload) -> Payload:
        if payload.key_pressed == self.toggle_key:
            self.is_on = not self._is_on
        elif payload.key_pressed in self.subscribed_keys:
            self.subscribed_key_presses(payload.key_pressed, payload)


        if self._is_on:
            payload = self._execute(payload)

        return payload

    @abstractmethod
    def _execute(self, payload: Payload) -> Payload:
        pass

    def _is_on_changed(self, is_on):
        pass

    def subscribed_key_presses(self, key_pressed, payload):
        pass
