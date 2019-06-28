import rx
from rx import operators as op
import cv2
from imutils.video import FPS
from functools import partial
import logging

from builders.pipeline_builders import PipeLineBuilder
from commands.payload import Payload

logger = logging.getLogger(__name__)


class PipelineDirector(object):
    """"""

    def __init__(self, builder: PipeLineBuilder):
        """"""
        super().__init__()
        self.builder = builder

    def __repr__(self):
        return super().__repr__()

    @staticmethod
    def get_stream(url, observer, scheduler):
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            observer.on_error("Error opening video stream or file")

        fps = FPS().start()
        try:
            while cap.isOpened():
                is_read_success, raw_frame = cap.read()
                # Using the FPS for getting smooth video while waiting
                fps.update()
                fps.stop()
                wait_time = max(fps.fps(), 1)
                key = chr(cv2.waitKey(round(wait_time)) & 0xFF)
                is_q_pressed = key == 'q'

                if is_q_pressed:
                    break

                if is_read_success:
                    observer.on_next(Payload(frame=raw_frame, key_pressed=key))
                else:
                    observer.on_error('Failed to read video capture')
                    observer.on_completed()
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        observer.on_completed()

    def build(self, url):
        source_func = partial(self.get_stream, url)

        # noinspection PyTypeChecker
        source = rx.create(source_func)
        commands = self.builder.get_commands()

        operators = [op.map(cmd) for cmd in commands]
        pipeline = source.pipe(*operators)

        return pipeline
