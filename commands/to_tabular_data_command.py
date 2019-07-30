import pandas as pd
from collections import namedtuple
from commands.abstract_command import FrameCommand
from commands.payload import Payload

TrackingRowData = namedtuple('TrackingRowData', ['id', 'frame', 'x', 'y', 'w', 'h', 'label'])
DetectionRowData = namedtuple('DetectionRowData', ['frame', 'x', 'y', 'w', 'h'])


class TabularDataCommand(FrameCommand):
    """"""

    def __init__(self, policy_controller=None):
        """"""
        super().__init__(toggle_key='f', policy_controller=policy_controller)
        self.df_tracking = pd.DataFrame(columns=TrackingRowData._fields)
        self.df_detections = pd.DataFrame(columns=DetectionRowData._fields)
        self.is_on = True

    def __repr__(self):
        return super().__repr__()

    def _execute(self, payload: Payload) -> Payload:
        self.df_tracking = self.get_tracking_data(payload)
        self.df_detections = self.get_detection_data(payload)

        payload.dfs['tracking'] = self.df_tracking
        payload.dfs['detections'] = self.df_detections

        return payload

    def get_tracking_data(self, payload):
        tracking_boxes = payload.tracking_boxes
        rows = [TrackingRowData(id=b.identifier, frame=payload.i_frame, x=b.x, y=b.y, w=b.w, h=b.h, label=b.label)
                for b
                in tracking_boxes]
        curr_df_tracking = pd.DataFrame(rows)
        df_tracking = pd.concat([self.df_tracking, curr_df_tracking], sort=False) \
            .drop_duplicates(subset=['id', 'x', 'y']) \
            .reset_index(drop=True)

        return df_tracking

    def get_detection_data(self, payload):
        detection_boxes = [d.bounding_box for d in payload.vehicle_detections]
        rows = [DetectionRowData(frame=payload.i_frame, x=b.x, y=b.y, w=b.w, h=b.h)
                for b
                in detection_boxes]

        curr_df_detections = pd.DataFrame(rows)
        df_detections = pd.concat([self.df_detections, curr_df_detections], sort=False) \
            .drop_duplicates(subset=['x', 'y']) \
            .reset_index(drop=True)

        return df_detections
