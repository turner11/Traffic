# https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
# USAGE
# python yolo.py --image images/baggage_claim.jpg --yolo yolo-coco
from pathlib import Path
import numpy as np
import argparse
import time
import cv2
import os
import logging

logger = logging.getLogger(__name__)


class YoloDetector(object):
    """"""

    def __init__(self, labels_path, config_path, weights_path, min_confidence, threshold):
        """"""
        super().__init__()
        # load the COCO class labels our YOLO model was trained on
        self.labels = Path(labels_path).read_text().strip().split("\n")
        self.config_path = config_path
        self.weights_path = weights_path
        self.min_confidence = min_confidence
        self.threshold = threshold

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")

        # load our YOLO object detector trained on COCO dataset (80 classes)
        logger.debug('loading YOLO from disk...')
        self.net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    def detect(self, image_path):
        # load our input image and grab its spatial dimensions
        config_path = self.config_path
        min_confidence = self.min_confidence
        threshold = self.threshold
        net = self.net
        image = cv2.imread(image_path)

        colors = self.colors
        labels = self.labels

        (H, W) = image.shape[:2]

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        # show timing information on YOLO
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

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
                    classIDs.append(classID)

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
                color = [int(c) for c in colors[classIDs[i]]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # show the output image
        cv2.imshow("Image", image)


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    ap.add_argument("-y", "--yolo", required=True,
                    help="base path to YOLO directory")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold", type=float, default=0.3,
                    help="threshold when applyong non-maxima suppression")
    args = vars(ap.parse_args())

    labels_path = os.path.sep.join([args["yolo"], "coco.names"])
    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
    configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])
    image_path = args["image"]
    min_confidence = args["confidence"]
    threshold = args["threshold"]

    if Path(image_path).is_file():
        image_files = [image_path]
    else:
        image_files = Path(image_path).iterdir()

    detector = YoloDetector(labels_path,configPath, weightsPath, min_confidence, threshold)
    for curr_image in image_files:
        detector.detect(str(curr_image))
        cv2.waitKey(0)


if __name__ == '__main__':
    main()
