from commands.abstract_command import FrameCommand
from common import layers


class DetectCommand(FrameCommand):
    """"""


    def __init__(self, detector):
        """"""
        super().__init__()
        self.detector = detector


    @classmethod
    def get_layer_type(cls):
        return layers.RawDataProcessing.DETECTION

    def execute(self, frame_container):
        frame = frame_container.frame
        detections = self.detector.detect(frame)
        return detections
