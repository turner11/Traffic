from commands.abstract_command import FrameCommand


class TrackCommand(FrameCommand):
    """"""

    def __init__(self, tracker=None):
        """"""
        super().__init__(toggle_key='t')
        self._is_on = False
        self.tracker = tracker

    def _execute(self, payload):
        tracker = self.tracker
        is_success, frame = tracker.track(payload.frame)

        should_reset = not is_success
        if should_reset:
            frame = payload.frame
            self._is_on = False
            tracker.reset()

        payload.frame = frame
        return payload

    def _is_on_changed(self, is_on):
        self.tracker.reset()
