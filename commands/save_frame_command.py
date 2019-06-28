import cv2
from commands.abstract_command import FrameCommand


class SaveFrameCommand(FrameCommand):
    """
    Command for saving a frame
    >>> fn = r'path\to\out_video.avi'
    >>> # initialize our video writer
    >>> fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    >>> video_writer = cv2.VideoWriter(fn, fourcc, 14, (720, 576), True)
    >>> SaveFrameCommand(video_writer=video_writer)
    >>> frames = [...]
    >>> for frame in frames:
    >>>     SaveFrameCommand._execute(frame)
    >>> video_writer.release()
    """

    def __init__(self, video_writer):
        """"""
        super().__init__('c')
        self.video_writer = video_writer

    def _execute(self, payload):
        frame = payload.frame
        self.video_writer.write(frame)
        payload.frame = frame
        return payload
