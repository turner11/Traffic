from collections import namedtuple
from functools import partial
import cv2
import rx
from rx import operators as op
import logging
from imutils.video import FPS

from trackers.opencv_tracker import OpenCvTracker
from yolo_detectors.yolo import YoloDetector

logger = logging.getLogger(__name__)
KeyAndFrame = namedtuple('KeyAndFrame', ['key', 'frame'])


class Orchestrator(object):
    """"""

    def __init__(self, url, yolo):
        """"""
        super().__init__()
        self.url = url
        self.yolo = yolo

        self._should_track = False

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
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        observer.on_completed()

    def start(self):
        url = self.url
        source_func = partial(self.get_stream, url)
        # noinspection PyTypeChecker
        source = rx.create(source_func)

        detector = YoloDetector.factory(yolo=self.yolo)
        tracker = OpenCvTracker()

        def track(key_and_frame):
            should_reset = False
            if key_and_frame.key == 's':
                if self._should_track:
                    should_reset = True

                self._should_track = not self._should_track


            if self._should_track:
                is_success , frame = tracker.track(key_and_frame.frame)
                should_reset = not is_success
            else:
                frame = key_and_frame.frame

            if should_reset:
                frame = key_and_frame.frame
                self._should_track = False
                tracker.reset()

            return KeyAndFrame(key_and_frame.key, frame)

        composed = source.pipe(
            op.map(lambda kf: KeyAndFrame(kf.key, detector.detect(kf.frame))),
            op.map(track),
        )

        composed.subscribe(on_next=lambda kf: cv2.imshow('Boxed Frames', kf.frame),
                           on_completed=lambda: logger.debug("Stream ended"),
                           on_error=lambda e: logger.exception('Got on error'))


