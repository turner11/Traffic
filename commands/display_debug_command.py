from commands.abstract_command import FrameCommand


class DisplayDebugCommand(FrameCommand):
    """"""

    def __init__(self):
        """"""
        super().__init__(toggle_key='g')
        self.is_on = True

    def _execute(self, payload):
        payload.debug_string = '\n'.join(f"{k}: {v}" for k,v in payload.debug_data.items())
        return payload
