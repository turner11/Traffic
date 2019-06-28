import cv2
import logging

from observers.abstract_observer import ObserverBase

logger = logging.getLogger(__name__)


class ShowObserver(ObserverBase):

    def __init__(self, title):
        """"""
        super().__init__()
        self.title = title

    def on_next(self, payload):
        frame = payload.frame
        cv2.imshow(self.title, frame)

