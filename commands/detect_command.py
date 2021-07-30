import pandas as pd
from dataclasses import dataclass
from commands.abstract_command import FrameCommand


@dataclass
class DetectionRowData:
    frame: int
    x: int
    y: int
    w: int
    h: int
    label: str


# DetectionRowData = namedtuple('DetectionRowData', ['frame', 'x', 'y', 'w', 'h', 'label'])

class DetectCommand(FrameCommand):
    """"""
    VEHICLE_LABELS = {'motorbike', 'truck', 'bus', 'car'}

    def __init__(self, detector, policy_controller=None):
        """"""
        super().__init__(toggle_key='d', policy_controller=policy_controller)
        self.detector = detector

        self.df_detections = pd.DataFrame(columns=DetectionRowData.__dataclass_fields__.keys())

    def _execute(self, payload):
        frame = payload.frame
        detections = self.detector.detect(frame)
        payload.detections = detections

        self.df_detections = self.get_session_detection_data(detections, payload.i_frame)
        payload.set_session_df('detections', self.df_detections)
        return payload

    def get_session_detection_data(self, detections, i_frame):
        vehicle_detections = [detection for detection in detections if detection.label in self.VEHICLE_LABELS]

        rows = [DetectionRowData(frame=i_frame,
                                 x=d.bounding_box.x, y=d.bounding_box.y, w=d.bounding_box.w, h=d.bounding_box.h,
                                 label=d.label)
                for d
                in vehicle_detections]

        curr_df_detections = pd.DataFrame(rows)
        df_detections = pd.concat([self.df_detections, curr_df_detections], sort=False) \
            .drop_duplicates(subset=['x', 'y']) \
            .reset_index(drop=True)

        return df_detections
