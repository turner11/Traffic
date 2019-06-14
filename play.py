import argparse
from collections import namedtuple

import imutils
import pandas as pd
import cv2
import logging

from imutils.video import FPS

from orchastrator import Orchstrator
from settings.all_cameras import data as cameras_dict
from yolo_object_detection import yolo as yolo_api
from utils import init_log

logger = logging.getLogger(__name__)

def play(url, yolo_detector=None):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        logger.warning("Error opening video stream or file")

    # Trained XML classifiers describes some features of some object we want to detect
    # car_cascade = cv2.CascadeClassifier('cars.xml')

    detect_generator = yolo_api.detect_gen(yolo=yolo_detector)
    # next(detect_generator)

    # just for debugging
    show_raw = False

    # Playing with tracking
    initBB = None
    fps = None
    tracker = None
    tracker_name = 'csrt'

    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        is_read_success, raw_frame = cap.read()

        if not is_read_success:
            logger.error('Failed to read video capture')
            break
        else:
            key = cv2.waitKey(1) & 0xFF


            if show_raw:
                output_frame = raw_frame
            else:
                next(detect_generator)
                # raw_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
                output_frame = detect_generator.send(raw_frame)

            # else:
            #     output_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
            #     # Detects cars of different sizes in the input image
            #     cars = car_cascade.detectMultiScale(output_frame, 1.1, 1)
            #
            #     # To draw a rectangle in each cars
            #     for (x, y, w, h) in cars:
            #         cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Press Q on keyboard to  exit

            is_q_pressed = key == ord('q')
            if is_q_pressed:
                break

            is_s_pressed = key == ord('s')
            if is_s_pressed:
                initBB = cv2.selectROI("Frame", output_frame, fromCenter=False, showCrosshair=True)
                tracker = OPENCV_OBJECT_TRACKERS[tracker_name]()
                tracker.init(output_frame, initBB)
                fps = FPS().start()


            if initBB is not None:# Are we tracking?
                # grab the new bounding box coordinates of the object
                (success, box) = tracker.update(output_frame)

                # check to see if the tracking was a success
                if success:
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(output_frame, (x, y), (x + w, y + h),(0, 255, 0), 2)

                # update the FPS counter
                fps.update()
                fps.stop()

                # initialize the set of information we'll be displaying on
                # the frame
                info = [
                    ("Tracker", tracker_name),
                    ("Success", "Yes" if success else "No"),
                    ("FPS", "{:.2f}".format(fps.fps())),
                ]

                output_frame = imutils.resize(output_frame, width=500)
                (H, W) = output_frame.shape[:2]
                # loop over the info tuples and draw them on our frame
                for (i, (k, v)) in enumerate(info):
                    text = "{}: {}".format(k, v)
                    color = (0, 255, 0) if success else (0, 0, 255)
                    cv2.putText(output_frame, text, (10, H - ((i * 20) + 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Display the resulting frame
            # cv2.imshow('Raw Frame', raw_frame)
            cv2.imshow('Boxed Frames', output_frame)
        # Break the loop

    # When everything done, release the video capture object
    cap.release()


# Closes all the frames
cv2.destroyAllWindows()


def get_url(camera_id: int = None):
    col_index, col_name, col_title, col_url = 'index', 'name', 'title', 'player_url_web'
    CameraInfo = namedtuple('CameraInfo', [col_index, col_name, col_title, col_url])
    all_cameras = [CameraInfo(i, d['name'], d['title'], d['player_url_web']) for i, d in enumerate(cameras_dict)]

    df = pd.DataFrame(all_cameras).set_index(col_index)

    if camera_id is None:
        print(df[[col_name, col_title]].to_string())
        camera_id = input('please select a camera (integer)')
        if camera_id.isdigit():
            camera_id = int(camera_id)

        min_id = min(df.index)
        max_id = max(df.index)
        while not isinstance(camera_id, int) or camera_id < min_id or max_id < camera_id:
            camera_id = input(f'input must be a valid integer between {min_id} and {max_id}')
            if camera_id.isdigit():
                camera_id = int(camera_id)

    selected_row = df.loc[camera_id]
    msg = f'using camera: {selected_row[col_name]}'
    logger.debug(msg)

    url = selected_row[col_url]
    return url


def main(camera_id=None, yolo=None):
    init_log()
    url = get_url(camera_id)
    # play(url, yolo_detector=yolo)
    orch = Orchstrator(url=url, yolo=yolo)
    orch.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c', dest='camera', help='the id of camera to use', required=False, default=None, type=int)
    parser.add_argument("-y", "--yolo", required=False, help="YOLO version or base path to YOLO directory",
                        default='v3')
    args = parser.parse_args()

    camera_id_arg = args.camera  # args.camera if args.camera >= 0 else None
    yolo_detector_arg = args.yolo
    main(camera_id=camera_id_arg, yolo=yolo_detector_arg)
