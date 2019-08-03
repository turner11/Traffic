from rx import operators as op

from commands.auto_track_command import AutoTrackCommand
from commands.collect_tracking_commands import TrackDetectionsCommand, ManualTrackingCommand
from commands.detect_command import DetectCommand
from commands.display_debug_command import DisplayDebugCommand
from commands.draw_bounding_box_command import DrawBoundingBoxCommand
from commands.draw_stats_command import DrawStatsCommand
from commands.median_command import MedianCommand
from commands.policy_controller import EveryNFramesPolicy
from commands.to_tabular_data_command import TabularDataCommand
from commands.track_command import TrackCommand
from common.exceptions import ArgumentException
from yolo_detectors.yolo_detector import YoloDetector


def _get_auto_track_operators(detector=None, tracker=None, **args):
    detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
    tracker = tracker
    cmd_auto_track = AutoTrackCommand(DetectCommand(detector), TrackCommand(tracker))
    raw_data_layers = [cmd_auto_track]
    output_layers = [
        # TabularDataCommand(),
        # MedianCommand()
    ]
    augmentation_layers = [DrawBoundingBoxCommand(), DisplayDebugCommand(), DrawStatsCommand()]
    commands = raw_data_layers + augmentation_layers + output_layers
    operators = [op.map(cmd) for cmd in commands]

    return operators


def _get_debug_operators(detector=None, tracker=None, **args):
    detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
    cmd_detect = DetectCommand(detector)
    cmd_track = TrackCommand(tracker)
    raw_data_layers = [cmd_detect, TrackDetectionsCommand(), ManualTrackingCommand(), cmd_track]
    augmentation_layers = [DrawBoundingBoxCommand(), DisplayDebugCommand(), DrawStatsCommand()]
    output_layers = []

    commands = raw_data_layers + augmentation_layers + output_layers
    operators = [op.map(cmd) for cmd in commands]

    return operators


def _get_road_roi_detector_operators(detector=None, tracker=None, **args):
    affective_detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
    if affective_detector is None:
        raise ArgumentException('Detector must be specified using the "detector" or "yolo" argument')

    str(tracker)

    detection_n_frames = 3 * 28
    median_n_frames = 1 * 28

    cmd_detect = DetectCommand(affective_detector, policy_controller=EveryNFramesPolicy(n=detection_n_frames))

    raw_data_layers = [cmd_detect]
    data_aggregation_layers = [TabularDataCommand(policy_controller=EveryNFramesPolicy(n=detection_n_frames))]
    processing_layers = [
         MedianCommand(policy_controller=EveryNFramesPolicy(n=median_n_frames))
    ]
    augmentation_layers = [DrawBoundingBoxCommand(), DisplayDebugCommand(), DrawStatsCommand()]

    commands = raw_data_layers + data_aggregation_layers + processing_layers + augmentation_layers
    operators = [op.map(cmd) for cmd in commands]

    return operators
