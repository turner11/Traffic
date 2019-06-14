import argparse
import time
import pandas as pd
import cv2
import logging

from settings.all_cameras import data as cameras_dict
from yolo_object_detection import yolo
from utils import init_log


logger = logging.getLogger(__name__)

davrat_url = 'https://5c328052cb7f5.streamlock.net/live/DAVRAT.stream/playlist.m3u8'
ahisemech_url = 'https://5c328052cb7f5.streamlock.net/live/AHISEMECH.stream/playlist.m3u8'


def play(url, yolo_detector=None):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        logger.warning("Error opening video stream or file")

    # Trained XML classifiers describes some features of some object we want to detect
    # car_cascade = cv2.CascadeClassifier('cars.xml')

    detect_generator = yolo.detect_gen(yolo=yolo_detector)
    # next(detect_generator)

    # just for debugging
    show_raw = False

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        is_read_success, raw_frame = cap.read()

        if not is_read_success:
            logger.error('Failed to read video capture')
            break
        else:

            if show_raw:
                output_frames = raw_frame
            else:
                next(detect_generator)
                # raw_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
                output_frames = detect_generator.send(raw_frame)

            # else:
            #     output_frames = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
            #     # Detects cars of different sizes in the input image
            #     cars = car_cascade.detectMultiScale(output_frames, 1.1, 1)
            #
            #     # To draw a rectangle in each cars
            #     for (x, y, w, h) in cars:
            #         cv2.rectangle(output_frames, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Display the resulting frame
            # cv2.imshow('Raw Frame', raw_frame)
            cv2.imshow('Boxed Frames', output_frames)

            # Press Q on keyboard to  exit
            is_q_pressed = cv2.waitKey(25) & 0xFF == ord('q')
            if is_q_pressed:
                break

        # Break the loop


    # When everything done, release the video capture object
    cap.release()


# Closes all the frames
cv2.destroyAllWindows()


def get_url(camera_id: int = None):
    col_name, col_title, col_url = 'name', 'title', 'player_url_web'
    all_camera_tpls = {i:(d['name'], d['title'], d['player_url_web']) for i, d in enumerate(cameras_dict)}

    df = pd.DataFrame(data=all_camera_tpls).transpose().rename(columns={0:col_name, 1:col_title, 2:col_url})


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
    # url = ahisemech_url  #davrat_url
    play(url, yolo_detector=yolo)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c', dest='camera', help='the id of camera to use', required=False, default=None, type=int)
    parser.add_argument("-y", "--yolo", required=False, help="YOLO version or base path to YOLO directory", default='v3')
    args = parser.parse_args()

    camera_id = args.camera#args.camera if args.camera >= 0 else None
    yolo_detector = args.yolo
    main(camera_id=camera_id, yolo=yolo_detector)



