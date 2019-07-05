from commands.abstract_command import FrameCommand

from detection_handlers.detection_drawer import draw_detections, draw_tracked_boxes


class DrawBoundingBoxCommand(FrameCommand):
    """"""

    def __init__(self):
        """"""
        super().__init__(toggle_key='b')
        self.is_on = True

    def _execute(self, payload):
        frame = payload.frame
        detections = payload.detections
        tracking_boxes = payload.tracking_boxes

        new_frame = draw_detections(frame, detections)
        new_frame = draw_tracked_boxes(new_frame, tracking_boxes)

        payload.frame = new_frame
        return payload
