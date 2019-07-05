import cv2
from imutils.video import FPS
from commands.abstract_command import FrameCommand


class DrawStatsCommand(FrameCommand):
    """"""

    def __init__(self):
        """
        :param additional_info: additional info to show
        """
        super().__init__(toggle_key='s')
        self.fps = None
        self.started = False

    def _execute(self, payload):
        frame = payload.frame
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
                   ] + list(payload.debug_data.items())

            # output_frame = imutils.resize(frame, width=500)
            (H, W) = frame.shape[:2]
            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                color = (0, 255, 0)
                org = (10, H - ((i * 20) + 20))
                font_scale = 0.4
                cv2.putText(frame, text, org, cv2.FONT_HERSHEY_SIMPLEX, font_scale , color, thickness=1)
        payload.frame = frame
        return payload

    def _is_on_changed(self, is_on):
        super()._is_on_changed(is_on)
        self.fps = None
        self.started = False
