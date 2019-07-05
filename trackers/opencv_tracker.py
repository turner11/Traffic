import cv2
from collections import OrderedDict, namedtuple

from common.types import BoundingBox

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
        self.trackers = []

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
        trackers = self.trackers

        results = {}
        boxes = {}
        for i, tracker in enumerate(trackers):
            # grab the new bounding box coordinates of the objects
            (success, box) = tracker.update(frame)
            results[tracker] = success

            # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                bb = BoundingBox(x, y, w, h)
                boxes[hash(tracker)] = bb
                cv2.rectangle(frame, bb.upper_left, bb.lower_right, (0, 255, 0), 1)

        for tracker, success in results.items():
            if not success:
                self.remove_tracker(tracker)

        success = len(results) == 0 or any(s for s in results.values())
        return success, frame

    def add_tracker(self, frame, bounding_box, tracker_name=None):
        # get the tracker
        tracker_name = tracker_name or self.tracker_name
        tracker = self._get_tracker(tracker_name)
        # Start tracking
        tracker.init(frame, bounding_box)
        self.trackers.append(tracker)

    def remove_tracker(self, tracker):
        tracker.clear()
        self.trackers.remove(tracker)

    def reset(self):
        for tracker in self.trackers:
            self.remove_tracker(tracker)
