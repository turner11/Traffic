import cv2

from commands.abstract_command import FrameCommand
from commands.collect_tracking_commands import TrackDetectionsCommand


class FindRoadRoiCommand(FrameCommand):
    """"""

    def __init__(self, detect_command, track_command, policy_controller=None):
        """"""
        super().__init__(toggle_key='a', policy_controller=policy_controller)
        self.detect_command = detect_command
        self.collect_command = TrackDetectionsCommand()
        self.track_command = track_command
        self.is_on = True

    def _execute(self, payload):
        pass
        return payload

    def get_debug_data(self) -> str:
        return super().get_debug_data()
