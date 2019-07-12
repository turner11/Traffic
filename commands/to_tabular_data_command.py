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
        self.df = pd.concat([self.df, curr_df], sort=False).drop_duplicates(subset=['id', 'x', 'y']) \
            .reset_index(drop=True)
        self.frame_count += 1

        payload.df = self.df

        return payload
