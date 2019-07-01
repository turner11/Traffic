import cv2

from commands.abstract_command import FrameCommand
from trackers.opencv_tracker import OpenCvTracker


class TrackCommand(FrameCommand):
    """"""

    def __init__(self, tracker=None):
        """"""
        super().__init__(toggle_key='r')
        self.tracker = tracker or OpenCvTracker()
        self.bounding_boxes = []

    def _execute(self, payload):
        tracker = self.tracker
        frame = payload.frame

        for init_bounding_box in payload.tracking_rois:
            self.tracker.add_tracker(frame, init_bounding_box)

        is_success, frame = tracker.track(frame)

        should_reset = not is_success
        if should_reset:
            frame = payload.frame
            self._is_on = False
            tracker.reset()

        payload.frame = frame
        return payload

    def _is_on_changed(self, is_on):
        self.tracker.reset()
