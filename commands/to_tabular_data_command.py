import pandas as pd
from collections import namedtuple

from commands.abstract_command import FrameCommand
from commands.payload import Payload

RowData = namedtuple('RowData', ['id', 'frame', 'x', 'y', 'w', 'h'])


class TabularDataCommand(FrameCommand):
    """"""

    def __init__(self):
        """"""
        super().__init__(toggle_key='f')
        self.df = pd.DataFrame(columns=RowData._fields)
        self.is_on = True
        self.frame_count = 0

    def __repr__(self):
        return super().__repr__()

    def _execute(self, payload: Payload) -> Payload:
        boxes = payload.tracking_boxes
        rows = [RowData(id=b.identifier, frame=self.frame_count, x=b.x, y=b.y, w=b.w, h=b.h) for b in boxes]
        curr_df = pd.DataFrame(rows)
        self.df = pd.concat([self.df, curr_df], sort=False).drop_duplicates(subset=['id', 'x', 'y'])\
                                                           .reset_index(drop=True)
        self.frame_count += 1

        plot = False
        if plot:
            import matplotlib.pyplot as plt
            import seaborn as sns
            sns.set(style="whitegrid")
            for group_id, group in self.df.groupby('id'):
                ax = sns.lineplot(x='x', y='y', data=group, estimator=None)#hue='id',
                ax.xaxis.set_ticks_position('top')

            # Plot the responses for different events and regions
            plt.ylim(max(self.df.y), 0)
            plt.show(block=True)


        return payload
