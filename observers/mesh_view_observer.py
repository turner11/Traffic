import cv2
import numpy as np
import logging

from commands.display_debug_command import DisplayDebugCommand
from commands.draw_stats_command import DrawStatsCommand
from observers.abstract_observer import ObserverBase

logger = logging.getLogger(__name__)


class MeshViewObserver(ObserverBase):

    def __init__(self, title):
        """"""
        super().__init__()
        self.title = title
        self.cmd_displayDebug = DisplayDebugCommand()
        self.cmd_drawStats = DrawStatsCommand()
    def on_next(self, payload):
        frame = payload.frame
        viewables = list(payload.viewables.values())
        viewables.insert(0, frame)

        if len(viewables) == 1:
            image = frame
        else:
            # Quick and dirty: make it always even.
            if len(viewables) % 2 != 0:
                viewables.append(frame)

            frame_shape = frame.shape
            scale = 1/len(viewables)
            new_size = tuple(int(v) for v in [frame_shape[0]*scale, frame_shape[1]*scale])
            processed = []
            for img in viewables:
                img = cv2.resize(img, new_size)

                # Make grey scale images have three channels
                if img.shape[-1] == 1:
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

                processed.append(img)

            items_in_row = 2
            res = []
            for i in range(items_in_row, len(processed)+items_in_row , items_in_row):
                items = processed[i-items_in_row: items_in_row]
                horizontal_stacked = np.hstack(items)
                if len(res) > 0:
                    res = np.vstack((res, horizontal_stacked))
                else:
                    res = horizontal_stacked

            image = res

        payload.frame = image
        payload = self.cmd_displayDebug.execute(payload)
        payload = self.cmd_drawStats.execute(payload)

        cv2.namedWindow(self.title, cv2.WINDOW_NORMAL)
        cv2.imshow(self.title, payload.frame)

