import cv2
import logging
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

    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        is_read_success, raw_frame = cap.read()
        if not is_read_success:
            logger.error('Failed to read video capture')
            break
        else:
            gray_frames = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2GRAY)
            # Detects cars of different sizes in the input image
            cars = car_cascade.detectMultiScale(gray_frames, 1.1, 1)

            # To draw a rectangle in each cars
            for (x, y, w, h) in cars:
                cv2.rectangle(gray_frames, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Display the resulting frame
            cv2.imshow('Raw Frame', raw_frame)
            cv2.imshow('Boxed Frames', gray_frames)

            # Press Q on keyboard to  exit
            is_q_pressed = cv2.waitKey(25) & 0xFF == ord('q')
            if is_q_pressed:
                break

        # Break the loop


    # When everything done, release the video capture object
    cap.release()


# Closes all the frames
cv2.destroyAllWindows()


def main():
    init_log()
    url = ahisemech_url #davrat_url
    play(url)


if __name__ == '__main__':
    main()
