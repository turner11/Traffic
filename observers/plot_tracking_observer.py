import logging
import pandas as pd
from observers.abstract_observer import ObserverBase

from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")
logger = logging.getLogger(__name__)


class PlotTrackingObserver(ObserverBase):

    def __init__(self):
        """"""
        super().__init__()
        self.lines = defaultdict(lambda: None)

        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()

        fig = plt.figure()#(figsize=(13, 6))
        self.ax = fig.add_subplot(111)
        self.ax.xaxis.set_ticks_position('top')
        plt.ion()
        plt.show()

    def on_next(self, payload):
        df = payload.get_session_df('tracking', pd.DataFrame())
        if len(df) > 0:
            plt.title(f'{len(df["id"].drop_duplicates())} tracked items')

            # adjust limits
            max_y = max(df.y)
            max_x = max(df.x)
            plt.ylim(max_y, 0)
            plt.xlim(0, max_x)

            # frame = payload.original_frame
            # self.ax.imshow(frame, extent=[0, max_x, 0, max_y])
            # return

            for group_id, group in df.groupby('id'):
                line = self.lines.get(group_id)
                x_vec = list(group.x.values)
                y1_data = list(group.y.values)
                if not line:
                    # create a variable for the line so we can later update it
                    line, = self.ax.plot(x_vec, y1_data, '-o', alpha=0.8, markersize=1)
                    self.lines[group_id] = line
                else:
                    # after the figure, axis, and line are created, we only need to update the y-data
                    line.set_xdata(x_vec)
                    line.set_ydata(y1_data)

            pause_time = 0.00000001
            plt.pause(pause_time)

            # plt.show(block=True)

    def on_completed(self):
        super().on_completed()
