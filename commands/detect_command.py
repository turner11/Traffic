from commands.abstract_command import FrameCommand


class DetectCommand(FrameCommand):
    """"""

    def __init__(self, detector):
        """"""
        super().__init__('d')
        self.detector = detector

    def _execute(self, payload):
        frame = payload.frame
        detections = self.detector.detect(frame)
        payload.detections = detections
        return payload
