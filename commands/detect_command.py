from commands.abstract_command import FrameCommand


class DetectCommand(FrameCommand):
    """"""

    def __init__(self, detector):
        """"""
        super().__init__()
        self.detector = detector

    def execute(self, frame_container):
        frame = frame_container.frame
        detections = self.detector.detect(frame)
        return detections
