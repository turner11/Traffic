import logging
import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from observers.abstract_observer import ObserverBase

sns.set(style="whitegrid")
logger = logging.getLogger(__name__)


class PlotDetectionsObserver(ObserverBase):

    def __init__(self):
        """"""
        super().__init__()
        self.lines = defaultdict(lambda: None)

        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()

        fig = plt.figure()  # (figsize=(13, 6))
        self.ax = fig.add_subplot(111)
        self.ax.xaxis.set_ticks_position('top')
        plt.ion()
        plt.show()

    def on_next(self, payload):
        df = payload.get_session_df('detections', pd.DataFrame()).drop_duplicates()
        plt.title(f'{len(df)} Detections')

        h, w = payload.frame.shape[0], payload.frame.shape[1]
        plt.ylim(h, 0)
        plt.xlim(0, w)
        # if len(df) > 0:

        # df['frame'] = df.frame.astype('category')
        # sns.scatterplot(x='x', y='y', hue='frame', data=df)
        # sns.scatterplot(x='x', y='y', data=df)

        # adjust limits
        # max_y = max(df.y)
        # max_x = max(df.x)

        vehicle_detections = list(payload.vehicle_detections)

        boxes = [d.bounding_box for d in vehicle_detections]
        # boxes = (b.get_scaled(0.5) for b in boxes)

        # This does a pretty good job at catching bottom of vehicle
        # from common.types import BoundingBox
        # boxes = (BoundingBox(b.x, b.y + b.h, b.w, int(round(b.h * 0.2))) for b in boxes)

        for box in boxes:
            # Create a Rectangle patch
            rect = patches.Rectangle((box.x, box.y), box.w, box.h, linewidth=1, edgecolor='r', facecolor='black')

            # Add the patch to the Axes
            self.ax.add_patch(rect)

        if len(boxes):
            pause_time = 0.0000001
            plt.pause(pause_time)

    def on_completed(self):
        super().on_completed()
