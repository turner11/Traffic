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
    >>>     SaveFrameCommand.execute(frame)
    >>> video_writer.release()
    """

    def __init__(self, video_writer):
        """"""
        super().__init__()
        self.video_writer = video_writer

    def execute(self, frame_container):
        frame = frame_container.frame
        self.video_writer.write(frame )
        return frame

