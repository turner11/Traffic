from collections import OrderedDict

import cv2

OPENCV_OBJECT_TRACKERS = OrderedDict([
    ('csrt', cv2.TrackerCSRT_create),
    ('kcf', cv2.TrackerKCF_create),
    ('mosse', cv2.TrackerMOSSE_create),
    ('boosting', cv2.TrackerBoosting_create),
    ('mil', cv2.TrackerMIL_create),
    ('tld', cv2.TrackerTLD_create),
    ('medianflow', cv2.TrackerMedianFlow_create),
    ]
)


# KCF: Fast and accurate
# CSRT: More accurate than KCF but slower
# MOSSE: Extremely fast but not as accurate as either KCF or CSRT


class OpenCvTracker(object):
    """"""

    def __init__(self, tracker: str = None):
        """"""
        super().__init__()
        self.tracker_name = tracker
        self.multi_tracker = None
        self.started_tracking = False

    @staticmethod
    def _get_tracker(tracker=None):
        if tracker:
            ctor = OPENCV_OBJECT_TRACKERS[tracker]
        else:
            tracker_name, ctor = list(OPENCV_OBJECT_TRACKERS.items())[0]

        instance = ctor()
        return instance

    def __repr__(self):
        return f'{self.__class__.__name__}(tracker={self.tracker_name})'

    def track(self, frame) -> (object, bool):
        if self.multi_tracker is None:
            self.multi_tracker = cv2.MultiTracker_create()

        trackers = self.multi_tracker

        # grab the new bounding box coordinates of the objects
        (success, boxes) = trackers.update(frame)

        # check to see if the tracking was a success
        if success:
            for box in boxes:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        else:
            self.reset()

        return success, frame

    def add_tracker(self, frame, init_bounding_box):
        tracker = self._get_tracker(self.tracker_name)
        self.multi_tracker.add(tracker, frame, init_bounding_box)
        self.started_tracking = True

    def reset(self):
        self.started_tracking = False
        if self.multi_tracker is None:
            self.multi_tracker.clear()
            self.multi_tracker = None
