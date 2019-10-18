from rx import operators as op

from commands.auto_track_command import AutoTrackCommand
from commands.collect_tracking_commands import SetDetectionsForTrackingCommand, ManualTrackingCommand
from commands.detect_command import DetectCommand
from commands.draw_bounding_box_command import DrawBoundingBoxCommand
from commands.filter_detections_command import FilterDetectionCommandByRois
from commands.find_road_roi_command import FindRoadRoiCommand
from commands.invalidate_trackers_command import InvalidateTrackersCommand
from commands.policy_controller import EveryNSecondsPolicy, DelayedStartPolicy  # EveryNFramesPolicy
from commands.track_command import TrackCommand
from common.exceptions import ArgumentException
from yolo_detectors.yolo_detector import YoloDetector


# from commands.display_debug_command import DisplayDebugCommand
# from commands.draw_stats_command import DrawStatsCommand
# from commands.median_command import MedianCommand


def append_augmentation_commands(func):
    def wrapper(*args, **kwargs):
        augmentation_operators = [op.map(cmd) for cmd
                                  in (DrawBoundingBoxCommand(),)]
        operators = func(*args, **kwargs)
        return operators + augmentation_operators

    return wrapper


@append_augmentation_commands
def _get_auto_track_operators(detector=None, tracker=None, **args):
    detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
    tracker = tracker
    cmd_auto_track = AutoTrackCommand(DetectCommand(detector), TrackCommand(tracker))
    raw_data_layers = [cmd_auto_track]
    output_layers = [
        # TabularDataCommand(),
        # MedianCommand()
    ]
    commands = raw_data_layers + output_layers
    operators = [op.map(cmd) for cmd in commands]

    return operators


@append_augmentation_commands
def _get_debug_operators(detector=None, tracker=None, **args):
    detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
    cmd_detect = DetectCommand(detector)
    cmd_track = TrackCommand(tracker)
    raw_data_layers = [cmd_detect, SetDetectionsForTrackingCommand(), ManualTrackingCommand(), cmd_track]

    commands = raw_data_layers
    operators = [op.map(cmd) for cmd in commands]

    return operators


@append_augmentation_commands
def _get_road_roi_detector_operators(detector=None, tracker=None, **args):
    affective_detector = detector or YoloDetector.factory(yolo=args.get('yolo'))
    if affective_detector is None:
        raise ArgumentException('Detector must be specified using the "detector" or "yolo" argument')

    str(tracker)

    detection_n_seconds = 3
    delay_seconds = 60.

    cmd_detect = DetectCommand(affective_detector, policy_controller=EveryNSecondsPolicy(n=detection_n_seconds))

    raw_data_layers = [cmd_detect]

    processing_layers = [
        # MedianCommand(policy_controller=EveryNFramesPolicy(n=median_n_frames)),
        FindRoadRoiCommand(),
        FilterDetectionCommandByRois(),
        SetDetectionsForTrackingCommand(),
        TrackCommand(tracker, policy_controller=DelayedStartPolicy(n_seconds=delay_seconds)),
        InvalidateTrackersCommand(policy_controller=DelayedStartPolicy(n_seconds=delay_seconds))

    ]

    commands = raw_data_layers + processing_layers

    for cmd in commands:
        cmd.is_on = True

    operators = [op.map(cmd) for cmd in commands]

    return operators