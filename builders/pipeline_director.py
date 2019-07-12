from pathlib import Path

import rx
from rx import operators as op
import cv2
from imutils.video import FPS
from functools import partial
import logging

from builders.pipeline_builders import PipeLineBuilder
from observers.observer_composition import ObserverComposition
from observers.plot_observer import PlotObserver
from observers.save_observer import SaveObserver
from observers.show_observer import ShowObserver
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

    # noinspection PyUnusedLocal
    @staticmethod
    def get_stream(url, observer, scheduler):
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            observer.on_error("Error opening video stream or file")

        fps = FPS().start()
        i_frame = -1
        try:
            while cap.isOpened():
                is_read_success, raw_frame = cap.read()
                if is_read_success:
                    i_frame += 1
                    # Using the FPS for getting smooth video while waiting
                    fps.update()
                    fps.stop()
                    if True or i_frame % 5 == 0:
                        wait_time = round(max(fps.fps(), 1))
                        key = chr(cv2.waitKey(wait_time) & 0xFF)
                        is_q_pressed = key == 'q'

                        if is_q_pressed:
                            break

                        observer.on_next(Payload(frame=raw_frame, key_pressed=key, i_frame=i_frame))

                else:
                    observer.on_error('Failed to read video capture')
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        observer.on_completed()

    def build(self, url, title='', save_folder=None):
        source_func = partial(self.get_stream, url)

        # noinspection PyTypeChecker
        source = rx.create(source_func)
        commands = self.builder.get_commands()

        operators = [op.map(cmd) for cmd in commands]
        pipeline = source.pipe(*operators)

        observers = [ShowObserver(title), PlotObserver()]

        if save_folder:
            file_name = f'{save_folder}\\{Path(title).name}.avi'
            save_observer = SaveObserver(path=file_name, title=title)
            observers.append(save_observer)

        observer = ObserverComposition(observers=observers)

        return pipeline, observer
