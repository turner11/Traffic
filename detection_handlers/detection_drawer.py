import cv2
import numpy as np

# initialize a list of colors to represent each possible class label
np.random.seed(7)
max_label_count = 500
_colors = iter(np.random.randint(0, 255, size=(max_label_count, 3), dtype="uint8"))
color_by_label = {}


def draw_detection(frame, detection):
    """
    draw a bounding box rectangle and label on the image
    :param frame: the frame to draw on
    :param detection:
    """
    label = detection.label
    confidence = detection.confidence
    x = detection.x
    y = detection.y
    w = detection.w
    h = detection.h

    if label not in color_by_label:
        color_by_label[label] = next(_colors)
    raw_color = color_by_label[label]
    color = [int(c) for c in raw_color]

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    text = f"{label}: {confidence:.4f}"
    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    ## show the output image
    # cv2.imshow("Image", image)
    return frame
