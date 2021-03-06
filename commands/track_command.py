import cv2

from commands.abstract_command import FrameCommand
from trackers.opencv_tracker import OpenCvTracker


class TrackCommand(FrameCommand):
    """"""

    def __init__(self, tracker=None, policy_controller=None):
        """"""
        super().__init__(toggle_key='r', policy_controller=policy_controller)
        self.tracker = tracker or OpenCvTracker()
        self.bounding_boxes = []

    def _execute(self, payload):
        tracker = self.tracker
        frame = payload.frame

        for bounding_box in payload.tracking_rois:
            self.tracker.add_tracker(frame, tuple(bounding_box), label=bounding_box.label)

        is_success, boxes = tracker.track(frame)

        should_reset = not is_success
        if should_reset:
            self.is_on = False

        payload.tracking_boxes.extend(boxes)
        return payload

    def _is_on_changed(self, is_on):
        self.reset()

    def reset(self):
        self.tracker.reset()

    def get_debug_data(self) -> str:
        base_string = super().get_debug_data()
        return f'{base_string}; ({len(self.tracker)} trackers)'


