import cv2
import pandas as pd
from collections import namedtuple

from commands.abstract_command import FrameCommand
from trackers.opencv_tracker import OpenCvTracker

TrackingRowData = namedtuple('TrackingRowData', ['id', 'frame', 'x', 'y', 'w', 'h', 'label'])


class TrackCommand(FrameCommand):
    """"""

    def __init__(self, tracker=None, policy_controller=None):
        """"""
        super().__init__(toggle_key='r', policy_controller=policy_controller)
        self.tracker = tracker or OpenCvTracker()
        self.df_tracking = pd.DataFrame(columns=TrackingRowData._fields)

    def _execute(self, payload):
        tracker = self.tracker
        frame = payload.frame

        for bounding_box in payload.tracking_rois:
            tracker.add_tracker(frame, tuple(bounding_box), label=bounding_box.label)

        is_success, tracking_results = tracker.track(frame)
        boxes = [tr.bounding_box for tr in tracking_results]

        # TODO: experimental
        min_confidence, threshold = 0, 0
        confidences = [0.5 for b in boxes]
        boxes_as_list = [list(b) for b in boxes]
        idxs = cv2.dnn.NMSBoxes(boxes_as_list, confidences, min_confidence, threshold)
        idxs_to_remove = {tr.tracker_id for i, tr in enumerate(tracking_results) if i not in idxs}

        df_tracker_invalidation = payload.get_session_df('tracker_invalidation', pd.DataFrame())
        if len(df_tracker_invalidation):
            idxs_to_remove = set(list(idxs_to_remove) + list(df_tracker_invalidation.id))

        idxs_to_remove = idxs_to_remove.intersection(set(tracker.trackers.keys()))

        for i in idxs_to_remove:
            tracker.remove_tracker(i)

        should_reset = not is_success
        if should_reset:
            self.is_on = False

        payload.tracking_boxes.extend(boxes)

        self.df_tracking = self.get_session_tracking_data(payload.tracking_boxes, payload.i_frame)
        payload.set_session_df('tracking', self.df_tracking)

        return payload

    def get_session_tracking_data(self, tracking_boxes, i_frame):

        rows = [TrackingRowData(id=b.identifier, frame=i_frame, x=b.x, y=b.y, w=b.w, h=b.h, label=b.label)
                for b
                in tracking_boxes]
        curr_df_tracking = pd.DataFrame(rows)
        df_tracking = pd.concat([self.df_tracking, curr_df_tracking], sort=False) \
            .reset_index(drop=True)
            # .drop_duplicates(subset=['id', 'x', 'y']) \

        return df_tracking

    def _is_on_changed(self, is_on):
        self.reset()

    def reset(self):
        self.tracker.reset()

    def get_debug_data(self) -> str:
        base_string = super().get_debug_data()
        return f'{base_string}; ({len(self.tracker)} trackers)'
