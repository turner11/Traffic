import logging
import cv2
from pathlib import Path

from common.exceptions import MissingFileException
# noinspection SpellCheckingInspection
from cv2.dnn import DNN_TARGET_OPENCL  # , DNN_TARGET_CPU, DNN_TARGET_FPGA, DNN_TARGET_MYRIAD

logger = logging.getLogger(__name__)


# you could try to set the env var: OPENCV_DNN_OPENCL_ALLOW_ALL_DEVICES=1

class YoloFolder(object):
    """Represents a folder contains yolo configuration"""
    CONFIG_FILE_PATTERN = r'yolov[0-9].cfg'
    CONFIG_LABELS_PATTERN = r'coco.names'
    CONFIG_WEIGHTS_PATTERN = r'yolo*.weights'

    def __init__(self, folder):
        """"""
        super().__init__()
        self.folder = Path(folder)

        def get_file(pattern):
            file_paths = list(self.folder.glob(pattern))
            if not len(file_paths) == 1:
                msg = f'expected to get as single file for pattern "{pattern}", ' \
                    f'but got {len(file_paths)} {file_paths}'
                raise MissingFileException(msg)
            path = file_paths[0]

            return path

        self.config_file = get_file(YoloFolder.CONFIG_FILE_PATTERN)
        self.weights_file = get_file(YoloFolder.CONFIG_WEIGHTS_PATTERN)
        self.labels_file = get_file(YoloFolder.CONFIG_LABELS_PATTERN)

        self.labels = Path(self.labels_file).read_text().strip().split("\n")

    def get_net(self, use_gpu=True):
        # load our YOLO object detector trained on COCO dataset (80 classes)
        logger.debug('loading YOLO from disk...')
        net = cv2.dnn.readNetFromDarknet(str(self.config_file), str(self.weights_file))

        if use_gpu:
            net.setPreferableTarget(DNN_TARGET_OPENCL)
        return net

    def __repr__(self):
        return f'{self.__class__.__name__}(folder={str(self.folder)})'
