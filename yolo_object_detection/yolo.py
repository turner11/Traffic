# https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
# USAGE
# python yolo.py --image images/baggage_claim.jpg --yolo yolo-coco
from pathlib import Path
from typing import Union

import numpy as np
import argparse
import time
import cv2
import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIDENCE = 0.5
DEFAULT_THRESHOLD = 0.3


class YoloDetector(object):
    """"""

    def __init__(self, labels_path: Union[str, Path],
                 config_path: Union[str, Path],
                 weights_path: Union[str, Path],
                 min_confidence: float = DEFAULT_CONFIDENCE,
                 threshold: float = DEFAULT_THRESHOLD) -> None:
        """
        :param labels_path: the path to labels file
        :param config_path: the coco v3 config
        :param weights_path: The coco v3 weights
        :param min_confidence: minimum probability to filter weak detections
        :param threshold: threshold when applying non-maxima suppression
        """
        super().__init__()
        # load the COCO class labels our YOLO model was trained on
        self.labels_path = str(labels_path)
        self.labels = Path(labels_path).read_text().strip().split("\n")

        self.config_path = str(config_path)
        self.weights_path = str(weights_path)

        self.min_confidence = min_confidence if min_confidence is not None else DEFAULT_CONFIDENCE
        self.threshold = threshold if threshold is not None else DEFAULT_THRESHOLD

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")

        # load our YOLO object detector trained on COCO dataset (80 classes)
        logger.debug('loading YOLO from disk...')
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(labels_path='{self.labels_path}', config_path='{self.config_path}', " \
            f"weights_path='{self.weights_path}', min_confidence={self.min_confidence}, threshold={self.threshold})"

    @staticmethod
    def factory(yolo_coco_path: Union[str, Path] = None,
                min_confidence: float = None,
                threshold: float = None):
        yolo_coco_path = Path(yolo_coco_path) if yolo_coco_path else Path(__file__).parent / 'yolo-coco'

        labels_path = yolo_coco_path / 'coco.names'
        config_path = yolo_coco_path / 'yolov3.cfg'
        weights_path = yolo_coco_path / 'yolov3.weights'

        assert all(p.exists() for p in [labels_path, config_path, weights_path])
        return YoloDetector(labels_path, config_path, weights_path, min_confidence, threshold)

    def detect_from_image_path(self, image_path, show=False):
        image = cv2.imread(image_path)
        return self.detect(image)

    def detect(self, image, show=False):
        # load our input image and grab its spatial dimensions
        min_confidence = self.min_confidence
        threshold = self.threshold
        net = self.net

        colors = self.colors
        labels = self.labels

        (H, W) = image.shape[:2]

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        # blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        # show timing information on YOLO
        logger.debug("YOLO took {:.6f} seconds".format(end - start))

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        class_ids = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability

                if confidence > min_confidence:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, threshold)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in colors[class_ids[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                class_id = class_ids[i]
                label = labels[class_id]
                text = "{}: {:.4f}".format(label, confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # show the output image
        if show:
            cv2.imshow("Image", image)
        return image


def detect_gen():
    detector = YoloDetector.factory()
    while True:
        frame = yield
        yield detector.detect(frame)


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    ap.add_argument("-y", "--yolo", required=True, help="base path to YOLO directory")
    ap.add_argument("-c", "--confidence", type=float, default=DEFAULT_CONFIDENCE,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="threshold when applyong non-maxima suppression")

    args = ap.parse_args()

    image_path = args.image
    min_confidence = args.confidence
    threshold = args.threshold

    if Path(image_path).is_file():
        image_files = [image_path]
    else:
        image_files = Path(image_path).iterdir()

    detector = YoloDetector.factory(args.yolo, min_confidence=min_confidence, threshold=threshold)
    # detector = YoloDetector(labels_path, configPath, weightsPath, min_confidence, threshold)
    for curr_image in image_files:
        detector.detect_from_image_path(str(curr_image), show=True)
        cv2.waitKey(0)


if __name__ == '__main__':
    main()
