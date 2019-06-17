from collections import namedtuple
from functools import partial
import cv2
import rx
from rx import operators as op
import logging
from imutils.video import FPS
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
        # noinspection PyTypeChecker
        source = rx.create(source_func)

        detector = YoloDetector.factory(yolo=self.yolo)
        tracker = OpenCvTracker()

        from commands.detect_command import DetectCommand
        from commands.draw_bonding_box_command import DrawBoundingBoxCommand
        from commands.track_command import TrackCommand
        from commands.draw_stats_command import DrawStatsCommand
        from commands.save_frame_command import SaveFrameCommand
        cmd_detect = DetectCommand(detector=detector)
        cmd_draw = DrawBoundingBoxCommand()
        cmd_track = TrackCommand(tracker)

        cmd_stats = DrawStatsCommand(additional_info={"Tracker": tracker.tracker})

        # fn = r'out_video.avi'
        # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        # video_writer = cv2.VideoWriter(fn, fourcc, 14, (720, 576), True)
        # cmd_save = SaveFrameCommand(video_writer=video_writer)

        composed = source.pipe(
            op.map(lambda kf: KeyFrameDetections(kf.key, kf.frame, cmd_detect(kf))),
            op.map(lambda kfd: KeyFrameDetections(kfd.key, cmd_draw(kfd), kfd.detections)),
            op.map(lambda kfd: KeyAndFrame(kfd.key, cmd_track(kfd))),
            op.map(lambda kfd: KeyAndFrame(kfd.key, cmd_stats(kfd)))
            # op.map(cmd_save)
        )

        composed.subscribe(on_next=lambda kf: cv2.imshow(f'Traffic: {self.yolo}', kf.frame),
                           on_completed=lambda: logger.debug("Stream ended"),
                           on_error=lambda e: logger.exception('Got on error'))
