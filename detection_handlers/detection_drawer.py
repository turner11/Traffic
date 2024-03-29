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


def draw_tracked_boxes(frame, tracked_bounding_boxes):
    for bounding_box in tracked_bounding_boxes:
        frame = draw_tracked_box(frame, bounding_box)
    return frame


def draw_tracked_box(frame, tracked_bounding_box):
    """
       draw a bounding box rectangle and label on the image
       :param frame: the frame to draw on
       :param tracked_bounding_box:
       """
    label = tracked_bounding_box.label
    text = f'{tracked_bounding_box.identifier} ({label})'.lower()
    color = static_colors.get(label,(0, 255, 0))
    frame = _draw_labeled_box(tracked_bounding_box, frame, text, color)
    return frame


def draw_detection(frame, detection):
    """
    draw a bounding box rectangle and label on the image
    :param frame: the frame to draw on
    :param detection:
    """
    label = detection.label.lower()
    raw_color = color_by_label[label]
    # noinspection PyTypeChecker
    color = [int(c) for c in raw_color]

    confidence = detection.confidence
    text = f"{label}: {confidence * 100:.0f}%"
    bounding_box = detection.bounding_box

    frame = _draw_labeled_box(bounding_box, frame, text, color)
    return frame


def _draw_labeled_box(bounding_box, frame, text, color=None):
    color = color or next(_colors)

    upper_left = bounding_box.upper_left
    lower_right = bounding_box.lower_right
    x = bounding_box.x
    y = bounding_box.y
    cv2.rectangle(frame, list(upper_left), list(lower_right), color, 1)
    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame
