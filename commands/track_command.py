from commands.abstract_command import FrameCommand


class TrackCommand(FrameCommand):
    """"""

    def __init__(self, tracker=None):
        """"""
        super().__init__()
        self.tracker = tracker
        self._should_track = False

    def execute(self, key_and_frame):
        tracker = self.tracker
        should_reset = False
        if key_and_frame.key == 's':
            if self._should_track:
                should_reset = True

            self._should_track = not self._should_track

        if self._should_track:
            is_success, frame = tracker.track(key_and_frame.frame)
            should_reset = not is_success
        else:
            frame = key_and_frame.frame

        if should_reset:
            frame = key_and_frame.frame
            self._should_track = False
            tracker.reset()

        return frame
