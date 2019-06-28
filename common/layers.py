from enum import auto, IntEnum


class RawDataProcessing(IntEnum):
    NONE = 0
    DETECTION = auto()
    TRACKING = auto()


class Augmentation(IntEnum):
    NONE = 0
    DETECTION_DRAWING = auto()
    STATISTICS = auto()


class OutPut(IntEnum):
    NONE = 0
    SCREEN = auto()
    FILE = auto()
