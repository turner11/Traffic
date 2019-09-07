from commands.abstract_command import FrameCommand
from commands.collect_tracking_commands import SetDetectionsForTrackingCommand


class AutoTrackCommand(FrameCommand):
    """"""

    def __init__(self, detect_command, track_command, policy_controller=None):
        """"""
        super().__init__(toggle_key='a', policy_controller=policy_controller)
        self.detect_command = detect_command
        self.collect_command = SetDetectionsForTrackingCommand()
        self.track_command = track_command
        self.is_on = True

    def _execute(self, payload):
        collect_detections = len(self.track_command.tracker) == 0

        if collect_detections:
            payload = self.detect_command._execute(payload)
            payload = self.collect_command._execute(payload)

        payload = self.track_command._execute(payload)
        return payload

    def get_debug_data(self) -> str:
        base_string = super().get_debug_data()
        return f'{base_string}; ({len(self.track_command.tracker)} trackers)'

    def _is_on_changed(self, is_on):
        self.track_command.reset()
