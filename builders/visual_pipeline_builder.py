from builders.runtime_pipeline_builder import RunTimePipelineBuilder
from common.layers import RawDataProcessing, Augmentation, OutPut
from trackers.opencv_tracker import OpenCvTracker
from yolo_detectors.yolo_detector import YoloDetector


class VisualPipelineBuilder(RunTimePipelineBuilder):
    """"""

    def __init__(self, detector=None, tracker=None):
        """"""
        self.detector = detector or YoloDetector.factory()
        self.tracker = tracker or OpenCvTracker()

        raw_data_layers = [RawDataProcessing.DETECTION ,RawDataProcessing.TRACKING]
        augmentation_layers = [Augmentation.DETECTION_DRAWING , Augmentation.STATISTICS]
        output_layers = [OutPut.SCREEN]
        super().__init__(raw_data_layers, augmentation_layers, output_layers)

    def __repr__(self):
        return super().__repr__()
