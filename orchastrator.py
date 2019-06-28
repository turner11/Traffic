from collections import namedtuple
from functools import partial
import cv2
import rx
from rx import operators as op
import logging
from imutils.video import FPS

from commands.show_command import ShowCommand
from trackers.opencv_tracker import OpenCvTracker
from yolo_detectors.yolo_detector import YoloDetector

logger = logging.getLogger(__name__)
KeyAndFrame = namedtuple('KeyAndFrame', ['key', 'frame'])
KeyFrameDetections = namedtuple('KeyAndFrame', ['key', 'frame', 'detections'])


class Orchestrator(object):
    """"""

    def __init__(self, url, yolo):
        """"""
        super().__init__()
        self.url = url
        self.yolo = yolo

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
                    observer.on_next(KeyAndFrame(key, raw_frame))
                else:
                    observer.on_error('Failed to read video capture')
                    observer.on_completed()
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        observer.on_completed()

    def start(self):
        url = self.url
        source_func = partial(self.get_stream, url)

        from builders.pipeline_director import PipelineDirector
        from builders.visual_pipeline_builder import VisualPipelineBuilder

        builder = VisualPipelineBuilder()
        director = PipelineDirector(builder)
        pipeline = director.build(source_func)

        pipeline.subscribe(on_next=lambda kf: kf,
                           on_completed=lambda: logger.debug("Stream ended"),
                           on_error=lambda e: logger.exception('Got on error'))
        # video_writer.release()
