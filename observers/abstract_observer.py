import logging
from abc import ABC, abstractmethod
from rx.core import Observer

logger = logging.getLogger(__name__)


class ObserverBase(Observer, ABC):
    """"""

    def __init__(self):
        """"""
        super().__init__()

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    @abstractmethod
    def on_next(self, payload):
        pass

    def on_completed(self):
        logger.debug("Stream ended")

    def on_error(self, error):
        logger.exception(f'Got an error: {error}')
