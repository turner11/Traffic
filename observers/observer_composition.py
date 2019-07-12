import logging

from observers.abstract_observer import ObserverBase

logger = logging.getLogger(__name__)


class ObserverComposition(ObserverBase):
    """"""

    def on_next(self, payload):
        for observer in self.observers:
            observer.on_next(payload)

    def on_completed(self):
        super().on_completed()
        for observer in self.observers:
            observer.on_completed()

    def on_error(self, error):
        super().on_error(error)
        for observer in self.observers:
            observer.on_error()

    def __init__(self, observers):
        """"""
        super().__init__()
        self.observers = observers

    def __repr__(self):
        return super().__repr__()
