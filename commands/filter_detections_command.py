import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from cv2 import cv2
from commands.abstract_command import FrameCommand
from image_process_helpers.road_roi_detector import get_rois


class FilterDetectionCommandByRois(FrameCommand):
    """"""

    def __init__(self, policy_controller=None):
        """"""
        super().__init__(toggle_key='f', policy_controller=policy_controller)
        self.is_on = True

    def _execute(self, payload):
        df_road_rois = payload.dfs.get('road_rois', pd.DataFrame())
        df_detections = payload.get_df_frame_detections()
        if len(df_road_rois) and len(df_detections):
            df_road_rois = df_road_rois.rename(columns={c:f'roi_{c}'for c in df_road_rois.columns})

            merged = df_detections.assign(key=1).merge(df_road_rois.assign(key=1), on='key',).drop('key', 1)
            idx_x_ok = (merged.x >= merged.roi_x) & (merged.x <= merged.roi_x2)
            idx_y_ok = (merged.y >= merged.roi_y) & (merged.y <= merged.roi_y2)
            is_ok = idx_x_ok & idx_y_ok
            df_in_roi = merged[is_ok][df_detections.columns].drop_duplicates()
        else:
            df_in_roi = pd.DataFrame()

        payload.dfs['df_detections'] = df_in_roi

        def is_detection_in_results(detection):
            b = detection.bounding_box
            return len(df_in_roi) > 0 and any((df_in_roi.x == b.x) & (df_in_roi.y == b.y))

        detections = [d for d in payload.detections if is_detection_in_results(d)]

        assert len(detections) == len(df_in_roi)
        payload.detections = detections
        return payload

    def get_debug_data(self) -> str:
        return super().get_debug_data()


