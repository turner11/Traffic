from pathlib import Path

import rx
import cv2
from imutils.video import FPS
from functools import partial
import logging

from tqdm import tqdm

from observers.mesh_view_observer import MeshViewObserver
from observers.observer_composition import ObserverComposition
from observers.plot_detections_observer import PlotDetectionsObserver
from observers.save_tabular_data_observer import SaveTabularDataObserver
from observers.save_video_observer import SaveVideoObserver
from observers.show_observer import ShowObserver
import time
from commands.payload import Payload

logger = logging.getLogger(__name__)


def _get_stream_fps(stream, num_frames=120):
    # Number of frames to capture

    fps = stream.get(cv2.CAP_PROP_FPS)
    return fps
    logging.debug(f"Capturing {num_frames} frames for fps calculation")
    # Start time
    start = time.time()

    # Grab a few frames
    for i in tqdm(range(0, num_frames)):
        ret, frame = stream.read()

    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    logging.debug(f"Time taken : {seconds:.4f} seconds")

    # Calculate frames per second
    fps = num_frames / seconds
    logging.debug(f"Estimated frames per second : {fps}")
    return fps


def url_to_source_function(url):
    def source_func(observer, scheduler):
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            observer.on_error("Error opening video stream or file")

        stream_fps = _get_stream_fps(cap)
        session = {'fps': stream_fps, 'dfs': {}}

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

                    wait_time = round(max(fps.fps(), 1))
                    key = chr(cv2.waitKey(wait_time) & 0xFF)
                    is_q_pressed = key == 'q'

                    if is_q_pressed:
                        break

                    payload = Payload(frame=raw_frame, session=session, key_pressed=key, i_frame=i_frame)
                    observer.on_next(payload)

                else:
                    observer.on_error('Failed to read video capture')
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        observer.on_completed()

    return source_func


def get_auto_track_pipeline(url, detector=None, tracker=None, **args):
    from pipelines._pipeline_operators import _get_auto_track_operators
    get_operators = partial(_get_auto_track_operators, detector=detector, tracker=tracker, **args)
    return _get_pipeline(get_operators, url, **args)


def get_debug_pipeline(url, detector=None, tracker=None, **args):
    from pipelines._pipeline_operators import _get_debug_operators
    get_operators = partial(_get_debug_operators, detector=detector, tracker=tracker, **args)
    return _get_pipeline(get_operators, url, **args)


def get_road_roi_pipeline(url, detector=None, tracker=None, **args):
    from pipelines._pipeline_operators import _get_road_roi_detector_operators
    get_operators = partial(_get_road_roi_detector_operators, detector=detector, tracker=tracker, **args)
    return _get_pipeline(get_operators, url, **args)


def _get_pipeline(get_operators, url, title=None, save_folder=None, **args):
    source_func = url_to_source_function(url)
    operators = get_operators()
    # noinspection PyTypeChecker
    source = rx.create(source_func)
    pipeline = source.pipe(*operators)

    observers = [MeshViewObserver(title),
                 # ShowObserver(title),
                 # PlotDetectionsObserver(),
                 # PlotTrackingObserver()
                 ]

    observer = ObserverComposition(observers=observers)
    # if save_folder:
    #     path = Path(save_folder)
    #
    #     file_name = path / (title + '.avi')
    #     save_video_observer = SaveVideoObserver(path=file_name, title=title)
    #     observers.append(save_video_observer)

    # file_name = path / 'detections.prqt'
    # save_data_observer = SaveTabularDataObserver(file_name)
    # observers.append(save_data_observer)

    return pipeline, observer
