import cv2
from commands.abstract_command import FrameCommand


class ShowCommand(FrameCommand):
    """"""

    def __init__(self, title):
        """"""
        super().__init__('v')
        self.title = title

    def _execute(self, payload):
        frame = payload.frame
        cv2.imshow(self.title, frame)
        return payload
