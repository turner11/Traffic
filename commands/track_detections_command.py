import cv2

from commands.abstract_command import FrameCommand
from trackers.opencv_tracker import OpenCvTracker


class TrackDetectionsCommand(FrameCommand):
    """"""

    def __init__(self):
        """"""
        super().__init__(toggle_key='t')
        self._is_on = False

    def _execute(self, payload):
        boxes = [(detection.x, detection.y, detection.w, detection.h) for detection in payload.detections]
        payload.tracking_rois.extend(boxes)

        # Don't start marking at every frame
        self._is_on = False
        return payload

