from commands.abstract_command import FrameCommand

from detection_handlers.detection_drawer import draw_detections


class DrawBoundingBoxCommand(FrameCommand):
    """"""

    def __init__(self):
        """"""
        super().__init__(toggle_key='b')
        self.is_on = True

    def _execute(self, payload):
        frame = payload.frame
        detections = payload.detections
        new_frame = draw_detections(frame, detections)
        payload.frame = new_frame
        return payload
