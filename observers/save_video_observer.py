from pathlib import Path

import cv2
import logging
from observers.show_observer import ShowObserver

logger = logging.getLogger(__name__)


class SaveVideoObserver(ShowObserver):

    def __init__(self, path, display_video=True, size=None, title='Saving stream'):
        """"""
        super().__init__(title)
        self.video_writer = None
        self.size = size
        self.path = Path(path)
        self.display_video = display_video

    def on_next(self, payload):
        if self.display_video:
            super().on_next(payload)

        frame = payload.frame
        if self.video_writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            self.size = self.size or (frame.shape[1], frame.shape[0])
            self.video_writer = cv2.VideoWriter(str(self.path), fourcc, 14, self.size, True)

        self.video_writer.write(frame)

    def on_completed(self):
        super().on_completed()
        if self.video_writer is not None:
            self.video_writer.release()


