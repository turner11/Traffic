from pathlib import Path
from typing import Union
import numpy as np
import argparse
import cv2
import logging

from common.types import BoundingBox, Detection
from yolo_detectors.configurations import yolo_detector_folders
from yolo_detectors.yolo_config_folder import YoloFolder

logger = logging.getLogger(__name__)

DEFAULT_CONFIDENCE = 0.5
DEFAULT_THRESHOLD = 0.3
DEFAULT_BLOB_SIZE = (480, 480)


# https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
class YoloDetector(object):
    """"""

    def __init__(self, yolo_folder: YoloFolder,
                 min_confidence: float = DEFAULT_CONFIDENCE,
                 threshold: float = DEFAULT_THRESHOLD,
                 blob_size: (int, int) = DEFAULT_BLOB_SIZE,
                 use_gpu: bool = True) -> None:
        """
        :param yolo_folder: the yolo folder instance
        :param min_confidence: minimum probability to filter weak detections
        :param threshold: threshold when applying non-maxima suppression
        """
        super().__init__()
        self.scale_factor = 1 / 255.0
        self.blob_size = blob_size
        # load the COCO class labels our YOLO model was trained on
        self.yolo_folder = yolo_folder
        self.labels_path = str(yolo_folder.labels_file)

        self.labels = self.yolo_folder.labels[:]

        self.min_confidence = min_confidence if min_confidence is not None else DEFAULT_CONFIDENCE
        self.threshold = threshold if threshold is not None else DEFAULT_THRESHOLD

        self.net = self.yolo_folder.get_net(use_gpu=use_gpu)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(yolo_folder='{self.yolo_folder}', " \
            f"min_confidence={self.min_confidence}, threshold={self.threshold})"

    @staticmethod
    def factory(yolo: Union[str, Path] = 'v3',
                min_confidence: float = None,
                threshold: float = None):

        yolo = yolo or 'v3'
        if isinstance(yolo, YoloFolder):
            logger.debug(f'Using yolo folder: {yolo}')
            yolo_folder = yolo
        else:
            if Path(yolo).exists():
                logger.debug(f'Using yolo folder: {yolo}')
                yolo_folder_path = Path(yolo)
            else:
                assert yolo in yolo_detector_folders.keys(), f'got an invalid yolo argument: {yolo}\n' \
                    f'Valid arguments are a yolo folder folder or: {list(yolo_detector_folders.keys())}'
                logger.debug(f'Using yolo: {yolo}')
                yolo_folder_path = yolo_detector_folders[yolo]

            yolo_folder = YoloFolder(yolo_folder_path)

        return YoloDetector(yolo_folder, min_confidence, threshold)

    def detect_from_image_path(self, image_path):
        image = cv2.imread(str(image_path))
        return self.detect(image)

    def detect(self, image):
        # load our input image and grab its spatial dimensions
        min_confidence = self.min_confidence
        threshold = self.threshold
        net = self.net
        labels = self.labels
        (H, W) = image.shape[:2]

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(image, scalefactor=self.scale_factor, size=self.blob_size, swapRB=True, crop=False)
        net.setInput(blob)

        layer_outputs = net.forward(ln)

        # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
        outputs = np.concatenate(layer_outputs)
        data_cols_count = 4
        boxes = outputs[:, :data_cols_count]
        scoresA = outputs[:, data_cols_count+1:]
        class_ids = np.argmax(scoresA, axis=1)


        row_count = scoresA.shape[0]
        confidences =  np.zeros(row_count)
        for row_idx in range(scoresA.shape[0]):
            idx = class_ids[row_idx]
            conf = scoresA[row_idx][idx]
            confidences[row_idx] = conf

        idxs = confidences > min_confidence
        scoresA, class_ids, confidences, boxes = [arr[idxs] for arr in [scoresA, class_ids, confidences, boxes]]
        # (centerX, centerY, width, height)
        detections = boxes  * np.array([W, H, W, H])
        centerX, centerY, width, height = [detections[:, i] for i in range(detections.shape[1])]
        # use the center (x, y)-coordinates to derive the top  left corner of the bounding box
        left = (centerX - (width / 2)).astype(int)
        top = (centerY - (height / 2)).astype(int)

        data = np.zeros((scoresA.shape[0], data_cols_count + 2))
        data[:, :data_cols_count] = np.asanyarray([left, top, width, height]).T
        data[:, data_cols_count]= confidences
        data[:, data_cols_count+1]= class_ids

        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        boxes = list(data[:, :data_cols_count].astype(int))
        confs = list(data[:, data_cols_count])
        idxs = cv2.dnn.NMSBoxes(boxes,confs , min_confidence, threshold)
        idxs = idxs.flatten() if len(idxs) else []
        detections = detections[idxs, :]

        # For now leaving for keeping same API
        detections_instances = []
        for i in range(data.shape[0]):
            row = data[i]
            x, y, width, height, conf, class_id = row
            bounding_box = BoundingBox(int(x), int(y), int(width), int(height))
            label = labels[int(class_id)]
            detection = Detection(label, bounding_box, float(conf))
            detections_instances.append(detection)

        return detections_instances


def detect_gen(yolo=None):
    detector = YoloDetector.factory(yolo=yolo)
    while True:
        frame = yield
        yield detector.detect(frame)


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="folder to input image")
    ap.add_argument("-y", "--yolo", required=True, help="YOLO version or base folder to YOLO directory")
    ap.add_argument("-c", "--confidence", type=float, default=DEFAULT_CONFIDENCE,
                    help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="threshold when applying non-maxima suppression")

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
        detector.detect_from_image_path(str(curr_image))
        cv2.waitKey(0)


if __name__ == '__main__':
    main()
