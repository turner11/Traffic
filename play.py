import time

import cv2
import logging

from settings.all_cameras import data as cameras_dict
from yolo_object_detection import yolo
from utils import init_log


logger = logging.getLogger(__name__)

davrat_url = 'https://5c328052cb7f5.streamlock.net/live/DAVRAT.stream/playlist.m3u8'
ahisemech_url = 'https://5c328052cb7f5.streamlock.net/live/AHISEMECH.stream/playlist.m3u8'


def play(url):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        logger.warning("Error opening video stream or file")

    # Trained XML classifiers describes some features of some object we want to detect
    car_cascade = cv2.CascadeClassifier('cars.xml')

    detect_generator = yolo.detect_gen()
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
                output_frames  = detect_generator.send(raw_frame)

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


def get_url():
    all_camera_tpls = {i:(d['name'], d['title'], d['player_url_web']) for i, d in enumerate(cameras_dict)}
    lines = [f'{key}: {tpl[0]} ({tpl[1]})' for key, tpl in all_camera_tpls.items()]
    txt = '\n'.join(lines)
    print(txt)

    arg = input('please select a camera (integer)')
    if arg.isdigit():
        arg = int(arg)

    valis_ids = all_camera_tpls.keys()
    min_id = min(valis_ids)
    max_id = max(valis_ids)
    while not isinstance(arg, int) or arg < min_id or max_id < arg:
        arg = input(f'input must be a valid integer between {min_id} and {max_id}')
        if arg.isdigit():
            arg = int(arg)

    tpl = all_camera_tpls[arg]
    url = tpl[2]
    return url




def main():
    init_log()
    url = get_url()
    # url = ahisemech_url  #davrat_url
    play(url)


if __name__ == '__main__':
    main()
