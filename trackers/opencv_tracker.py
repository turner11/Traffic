import cv2
import logging
import itertools
from typing import List, Tuple
from collections import OrderedDict

import numpy as np

from common.types import TrackedBoundingBox

OPENCV_OBJECT_TRACKERS = OrderedDict([
    ('csrt', cv2.TrackerCSRT_create),
    ('kcf', cv2.TrackerKCF_create),
    ('mil', cv2.TrackerMIL_create),

]
)
# Hack: missing package
try:
    OPENCV_OBJECT_TRACKERS += [
        ('mosse', cv2.TrackerMOSSE_create),
        ('boosting', cv2.TrackerBoosting_create),
        ('tld', cv2.TrackerTLD_create),
        ('medianflow', cv2.TrackerMedianFlow_create),
    ]
except Exception as ex:
    pass


# KCF: Fast and accurate
# CSRT: More accurate than KCF but slower
# MOSSE: Extremely fast but not as accurate as either KCF or CSRT
id_generator = itertools.count()

logger = logging.getLogger(__name__)
class TrackingResults(object):
    """"""

    def __init__(self, tracker_id, bounding_box):
        """"""
        super().__init__()
        self.tracker_id = tracker_id
        self.bounding_box = bounding_box

    def __repr__(self):
        return f'{self.__class__.__name__}(tracker_id={self.tracker_id}, bounding_box={self.bounding_box})'


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

    def track(self, frame: np.ndarray) -> Tuple[bool, List[TrackingResults]]:
        trackers = self.trackers

        results = []
        trackers_to_remove = []
        for tracker_id, tracker in trackers.items():
            # grab the new bounding box coordinates of the objects
            (success, box) = tracker.update(frame)
            if not success:
                trackers_to_remove.append(tracker_id)
                continue

            label = self.tracker_labels.get(tracker_id, '')

            (x, y, w, h) = [int(v) for v in box]
            bb = TrackedBoundingBox(tracker_id, label, x, y, w, h)
            results.append(TrackingResults(tracker_id, bb))

        for tracker_id in trackers_to_remove:
            self.remove_tracker(tracker_id)

        success = len(results) > 0 or len(trackers) == 0
        return success, results

    def add_tracker(self, frame, bounding_box, tracker_name=None, label=''):
        # get the tracker
        tracker_name = tracker_name or self.tracker_name
        tracker = self._get_tracker(tracker_name)
        # Start tracking
        tracker.init(frame, bounding_box)
        tracker_id = next(id_generator)
        self.trackers[tracker_id] = tracker
        self.tracker_labels[tracker_id] = label

    def remove_tracker(self, tracker_id):
        tracker = self.trackers[tracker_id]
        logger.debug(f'Clearing tracker ({tracker_id})')
        # tracker.clear()

        del self.trackers[tracker_id]

    def reset(self):
        for tracker in list(self.trackers.keys()):
            self.remove_tracker(tracker)


