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


class FindRoadRoiCommand(FrameCommand):
    """"""

    def __init__(self, policy_controller=None):
        """"""
        super().__init__(toggle_key='o', policy_controller=policy_controller)
        self.is_on = True
        self.detections_count = 0
        self.last_rois = pd.DataFrame()

    def _execute(self, payload):
        df_detections = payload.session['dfs'].get('detections', pd.DataFrame()).drop_duplicates()
        if self.detections_count < len(df_detections):
            self.detections_count = len(df_detections)
            df_extremes = get_rois(df_detections)
            self.last_rois = df_extremes

        payload.dfs['road_rois'] = self.last_rois

        if len(self.last_rois):
            # Add frame for debugging purposes
            frame = payload.frame
            from image_process_helpers.road_roi_detector import lay_rects_on_image
            marked_frame = lay_rects_on_image(frame, self.last_rois, filled=False)

            payload.viewables['road_rois'] = marked_frame


        return payload

    def get_debug_data(self) -> str:
        return super().get_debug_data()
