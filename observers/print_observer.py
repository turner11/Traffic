import logging

from observers.abstract_observer import ObserverBase

logger = logging.getLogger(__name__)


class PrintObserver(ObserverBase):

    def on_next(self, payload):
        logger.debug("Received {0}".format(payload))
