import cv2

from commands.abstract_command import FrameCommand
from detection_handlers.detection_drawer import draw_detections


class ShowCommand(FrameCommand):
    """"""

    def __init__(self, title):
        """"""
        super().__init__()
        self.title = title

    def execute(self, frame_container):
        frame = frame_container.frame
        cv2.imshow(self.title, frame)
        return frame
