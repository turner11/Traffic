from collections import defaultdict

import cv2
import numpy as np

# initialize a list of colors to represent each possible class label
np.random.seed(7)
max_label_count = 500
_colors = iter(np.random.randint(0, 255, size=(max_label_count, 3), dtype="uint8"))
static_colors = {'car': (255, 0, 0),
                 'truck': (0, 255, 255),
                 'bus': (127, 0, 255),
                 'person': (255, 0, 255),
                 'traffic light': (0, 255, 0), }
color_by_label = defaultdict(lambda: next(_colors))
# noinspection PyTypeChecker
color_by_label.update(static_colors)


def draw_detections(frame, detections):
    for detection in detections:
        frame = draw_detection(frame, detection)
    return frame


def draw_detection(frame, detection):
    """
    draw a bounding box rectangle and label on the image
    :param frame: the frame to draw on
    :param detection:
    """
    label = detection.label.lower()
    confidence = detection.confidence
    x = detection.x
    y = detection.y
    w = detection.w
    h = detection.h

    raw_color = color_by_label[label]
    # noinspection PyTypeChecker
    color = [int(c) for c in raw_color]

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
    text = f"{label}: {confidence * 100:.0f}%"
    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    ## show the output image
    # cv2.imshow("Image", image)
    return frame
