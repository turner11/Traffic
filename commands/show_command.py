import cv2
from commands.abstract_command import FrameCommand
from common import layers


class ShowCommand(FrameCommand):
    """"""


    def __init__(self, title):
        """"""
        super().__init__()
        self.title = title

    @classmethod
    def get_layer_type(cls):
        return layers.OutPut.SCREEN

    def execute(self, frame_container):
        frame = frame_container.frame
        cv2.imshow(self.title, frame)
        return frame
