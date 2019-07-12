import itertools

import cv2
from collections import OrderedDict

from common.types import TrackedBoundingBox

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
id_generator = itertools.count()

class OpenCvTracker(object):
    """"""

    def __init__(self, tracker: str = None):
        """"""
        super().__init__()
        self.tracker_name = tracker
        self.trackers = {}
        self.tracker_labels = {}

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

    def __len__(self):
        return len(self.trackers)

    def track(self, frame) -> (object, bool):
        trackers = self.trackers

        results = {}
        boxes = []
        for tracker_id, tracker in trackers.items():
            # grab the new bounding box coordinates of the objects
            (success, box) = tracker.update(frame)
            results[tracker] = success
            label = self.tracker_labels.get(tracker_id, '')

            # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                bb = TrackedBoundingBox(tracker_id, label, x, y, w, h)
                boxes.append(bb)

        for tracker, success in results.items():
            if not success:
                self.remove_tracker(tracker)

        success = len(results) == 0 or any(s for s in results.values())
        return success, boxes

    def add_tracker(self, frame, bounding_box, tracker_name=None, label=''):
        # get the tracker
        tracker_name = tracker_name or self.tracker_name
        tracker = self._get_tracker(tracker_name)
        # Start tracking
        tracker.init(frame, bounding_box)
        tracker_id = next(id_generator)
        self.trackers[tracker_id] = tracker
        self.tracker_labels[tracker_id] = label

    def remove_tracker(self, tracker):
        tracker.clear()
        for tracker_id, curr_tracker in list(self.trackers.items()):
            if tracker == curr_tracker:
                del self.trackers[tracker_id]

    def reset(self):
        for tracker in list(self.trackers.values()):
            self.remove_tracker(tracker)
