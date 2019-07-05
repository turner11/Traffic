from builders.runtime_pipeline_builder import RunTimePipelineBuilder

from yolo_detectors.yolo_detector import YoloDetector

from commands.display_debug_command import DisplayDebugCommand
from commands.collect_tracking_commands import TrackDetectionsCommand, ManualTrackingCommand
from commands.detect_command import DetectCommand
from commands.track_command import TrackCommand
from commands.draw_bounding_box_command import DrawBoundingBoxCommand
from commands.draw_stats_command import DrawStatsCommand


class FullPipelineBuilder(RunTimePipelineBuilder):
    """"""

    def __init__(self, detector=None, tracker=None, **args):
        """"""
        self.detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
        self.tracker = tracker

        raw_data_layers = [DetectCommand(self.detector), TrackDetectionsCommand(), ManualTrackingCommand(), TrackCommand(self.tracker)]
        augmentation_layers = [DrawBoundingBoxCommand(),DisplayDebugCommand(), DrawStatsCommand()]
        output_layers = []

        commands = raw_data_layers + augmentation_layers + output_layers
        super().__init__(commands)

    def __repr__(self):
        return super().__repr__()
