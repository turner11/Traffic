from commands.median_command import MedianCommand
from commands.policy_controller import EveryNFramesPolicy
from common.exceptions import ArgumentException
from yolo_detectors.yolo_detector import YoloDetector
from builders.abstract_pipeline_builders import RunTimePipelineBuilder

from commands.to_tabular_data_command import TabularDataCommand

from commands.display_debug_command import DisplayDebugCommand
from commands.detect_command import DetectCommand
from commands.draw_bounding_box_command import DrawBoundingBoxCommand
from commands.draw_stats_command import DrawStatsCommand


class RoadDetectorBuilder(RunTimePipelineBuilder):
    """"""

    def __init__(self, detector=None, **args):
        """"""
        affective_detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
        if affective_detector is None:
            raise ArgumentException('Detector must be specified using the "detector" or "yolo" argument')

        detection_n_frames = 3 * 28
        median_n_frames = 1 * 28

        cmd_detect = DetectCommand(affective_detector, policy_controller=EveryNFramesPolicy(n=detection_n_frames))

        raw_data_layers = [cmd_detect]
        data_aggregation_layers = [TabularDataCommand()]
        processing_layers = [MedianCommand(policy_controller=EveryNFramesPolicy(n=median_n_frames))]
        augmentation_layers = [DrawBoundingBoxCommand(), DisplayDebugCommand(), DrawStatsCommand()]

        commands = raw_data_layers + data_aggregation_layers + processing_layers + augmentation_layers
        super().__init__(commands)

    def __repr__(self):
        return super().__repr__()
