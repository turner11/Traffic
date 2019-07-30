from commands.abstract_command import FrameCommand


class DetectCommand(FrameCommand):
    """"""

    def __init__(self, detector, policy_controller=None):
        """"""
        super().__init__(toggle_key='d', policy_controller=policy_controller)
        self.detector = detector

    def _execute(self, payload):
        frame = payload.frame
        detections = self.detector.detect(frame)
        payload.detections = detections
        return payload
