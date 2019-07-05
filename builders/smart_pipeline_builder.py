from yolo_detectors.yolo_detector import YoloDetector
from builders.runtime_pipeline_builder import RunTimePipelineBuilder

from commands.auto_track_command import AutoTrackCommand
from commands.display_debug_command import DisplayDebugCommand
from commands.collect_tracking_commands import TrackDetectionsCommand, ManualTrackingCommand
from commands.detect_command import DetectCommand
from commands.track_command import TrackCommand
from commands.draw_bounding_box_command import DrawBoundingBoxCommand
from commands.draw_stats_command import DrawStatsCommand


class SmartPipelineBuilder(RunTimePipelineBuilder):
    """"""

    def __init__(self, detector=None, tracker=None, **args):
        """"""
        self.detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
        self.tracker = tracker

        cmd_auto_track = AutoTrackCommand(DetectCommand(self.detector), TrackCommand(self.tracker))

        from commands.to_tabular_data_command import TabularDataCommand
        raw_data_layers = [cmd_auto_track]
        output_layers = [TabularDataCommand()]
        augmentation_layers = [DrawBoundingBoxCommand(), DisplayDebugCommand(), DrawStatsCommand()]

        commands = raw_data_layers + augmentation_layers + output_layers
        super().__init__(commands)

    def __repr__(self):
        return super().__repr__()
