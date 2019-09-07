import cv2
from imutils.video import FPS
from commands.abstract_command import FrameCommand


class DrawStatsCommand(FrameCommand):
    """"""

    def __init__(self):
        super().__init__(toggle_key='s')
        self.fps = None
        self.started = False
        self.font = cv2.FONT_HERSHEY_TRIPLEX
        self.color = (0, 255, 0)
        self.font_scale = 0.4
        self.is_on = True

    def _execute(self, payload):
        frame = payload.frame
        debug_string = payload.debug_string
        if not self.started:
            self.fps = FPS().start()
            self.started = True
        else:
            fps = self.fps

            # update the FPS counter
            fps.update()
            fps.stop()

            info = [
                       ("FPS", "{:.2f}".format(fps.fps())),
                   ] + [('', debug_string)]

            (H, W) = frame.shape[:2]
            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v) if k else v
                for j, row_text in enumerate(text.split('\n')):
                    offset = ((i+j) * 20)
                    org = (10, H - (offset + 20))
                    cv2.putText(frame, row_text, org, self.font, self.font_scale, self.color, thickness=1)
        payload.frame = frame
        return payload

    def _is_on_changed(self, is_on):
        super()._is_on_changed(is_on)
        self.fps = None
        self.started = False
