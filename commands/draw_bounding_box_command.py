from commands.abstract_command import FrameCommand
from common import layers
from detection_handlers.detection_drawer import draw_detections


class DrawBoundingBoxCommand(FrameCommand):
    """"""


    def __init__(self):
        """"""
        super().__init__()

    @classmethod
    def get_layer_type(cls):
        return layers.Augmentation.DETECTION_DRAWING

    def execute(self, frame_and_detections):
        frame = frame_and_detections.frame
        detections = frame_and_detections.detections
        new_frame = draw_detections(frame, detections)
        return new_frame
