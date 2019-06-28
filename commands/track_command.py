import cv2

from commands.abstract_command import FrameCommand
from trackers.opencv_tracker import OpenCvTracker


class TrackCommand(FrameCommand):
    """"""
    KEY_ADD_BOUNDING_BOX = 'r'

    def __init__(self, tracker=None):
        """"""
        super().__init__(toggle_key='t', subscribed_keys=[self.KEY_ADD_BOUNDING_BOX])
        self._is_on = False
        self.tracker = tracker or OpenCvTracker()
        self.bounding_boxes = []

    def _execute(self, payload):
        tracker = self.tracker
        frame = payload.frame

        is_success, frame = tracker.track(frame)

        should_reset = not is_success
        if should_reset:
            frame = payload.frame
            self._is_on = False
            tracker.reset()

        payload.frame = frame
        return payload

    def subscribed_key_presses(self, key_pressed, payload):
        frame = payload.frame
        if key_pressed == self.KEY_ADD_BOUNDING_BOX:
            window_name = 'set tracking area'
            init_bounding_box = cv2.selectROI(window_name, frame, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow(window_name)

            has_bounding_box = any(v != 0 for v in init_bounding_box)
            if has_bounding_box:
                self.tracker.add_tracker(frame, init_bounding_box)
                self._is_on = True

    def _is_on_changed(self, is_on):
        self.tracker.reset()
