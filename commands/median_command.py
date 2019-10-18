import numpy as np
from cv2 import cv2

from commands.abstract_command import FrameCommand
from common.types import BoundingBox


class MedianCommand(FrameCommand):
    """"""

    def __init__(self, policy_controller=None):
        """"""
        super().__init__(toggle_key='m', policy_controller=policy_controller)
        self.is_on = True
        self.frames = []
        self.detection_mask = np.ndarray((0,))

    def _execute(self, payload):
        frame = payload.original_frame
        raw_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frames = self.frames
        median = np.median(frames, axis=0).astype(float) if len(frames) else np.ndarray((0,))  # .reshape(100, 100)

        if len(self.detection_mask) == 0:
            self.detection_mask = np.zeros(raw_gray.shape, dtype='uint8')

        # df = payload.dfs.get('detections', pd.DataFrame()).drop_duplicates()
        # if len(df) > 0:

        vehicle_detections = list(payload.detections)

        boxes = (d.bounding_box for d in vehicle_detections)
        # boxes = (b.get_scaled(0.5) for b in boxes)
        bb_h_percentage = 0.2
        boxes = [BoundingBox(b.x, int(round(b.y + b.h * (1 - bb_h_percentage))), b.w,
                             int(round(b.h * bb_h_percentage))) for b in boxes]
        for box in boxes:
            # y_start = max(0, box.y)
            # y_end = max(box.y + box.h, 0)
            # x_start = max(0, box.x)
            # x_end = max(0, box.x + box.w)
            # self.detection_mask[y_start: y_end, x_start:x_end] = 1
            self.detection_mask[box.y: box.y + box.h, box.x:box.x + box.w] = 1

        # cv2.imshow('detection_mask',self.detection_mask*255)
        # cv2.waitKey(0)

        gray = raw_gray.copy()  # * (1 - self.detection_mask)
        if len(median):
            idxs = np.where(self.detection_mask == 1)
            detections_median = np.median(median[idxs])
            gray[idxs] = detections_median

        self.frames.append(gray)
        payload.images['median'] = median
        if len(median):
            pass
            # title = 'Median'
            # cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            # cv2.imshow(title, median / 255)

        return payload
